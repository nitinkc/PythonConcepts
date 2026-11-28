import asyncio
import functools
import inspect
import logging
import time
import uuid
from contextvars import ContextVar
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

# Holds the active trace ID for the current async/thread execution context
trace_id_var: ContextVar[str] = ContextVar("trace_id", default="-")

def get_trace_id() -> str:
    return trace_id_var.get()

def set_trace_id(trace_id: str | None = None) -> str:
    tid = trace_id or str(uuid.uuid4())
    trace_id_var.set(tid)
    return tid

def _summarize_args(args: tuple[Any, ...], kwargs: dict[str, Any], max_len: int = 200) -> str:
    # Avoid dumping FastAPI Request/Session objects noisily; keep values compact
    safe_args = [
        f"<{type(a).__name__}>" if type(a).__module__.startswith("starlette") or type(a).__module__.startswith("fastapi") else repr(a)
        for a in args
    ]
    safe_kwargs = {
        k: f"<{type(v).__name__}>" if type(v).__module__.startswith("starlette") or type(v).__module__.startswith("fastapi") else repr(v)
        for k, v in kwargs.items()
    }
    raw = f"args=[{', '.join(safe_args)}] kwargs={safe_kwargs}"
    return raw if len(raw) <= max_len else raw[:max_len] + "...(truncated)"

def trace_log(
    logger: logging.Logger | None = None,
    level: int = logging.DEBUG,
    log_result: bool = False,
) -> Callable[[F], F]:
    """Decorator that logs entry, duration, and errors for sync and async functions."""

    def decorator(func: F) -> F:
        target_logger = logger or logging.getLogger(func.__module__)
        qualname = func.__qualname__

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            tid = get_trace_id()
            if tid == "-":
                tid = set_trace_id()

            start = time.perf_counter()
            arg_summary = _summarize_args(args, kwargs)

            target_logger.log(level, "[trace=%s] ENTER %s %s. Fucntion Name : %s", tid, qualname, arg_summary, func.__name__)
            try:
                result = await func(*args, **kwargs)
            except Exception as exc:
                elapsed_ms = (time.perf_counter() - start) * 1000
                target_logger.exception(
                    "[trace=%s] ERROR %s after %.2fms: %s",
                    tid,
                    qualname,
                    elapsed_ms,
                    exc,
                )
                raise
            else:
                elapsed_ms = (time.perf_counter() - start) * 1000
                if log_result:
                    target_logger.log(
                        level,
                        "[trace=%s] EXIT %s (%.2fms) result=%r",
                        tid,
                        qualname,
                        elapsed_ms,
                        result,
                    )
                else:
                    target_logger.log(
                        level,
                        "[trace=%s] EXIT %s (%.2fms)",
                        tid,
                        qualname,
                        elapsed_ms,
                    )
                return result

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            tid = get_trace_id()
            if tid == "-":
                tid = set_trace_id()

            start = time.perf_counter()
            arg_summary = _summarize_args(args, kwargs)
            target_logger.log(level, "[trace=%s] ENTER %s %s", tid, qualname, arg_summary)
            try:
                result = func(*args, **kwargs)
            except Exception as exc:
                elapsed_ms = (time.perf_counter() - start) * 1000
                target_logger.exception(
                    "[trace=%s] ERROR %s after %.2fms: %s",
                    tid,
                    qualname,
                    elapsed_ms,
                    exc,
                )
                raise
            else:
                elapsed_ms = (time.perf_counter() - start) * 1000
                if log_result:
                    target_logger.log(
                        level,
                        "[trace=%s] EXIT %s (%.2fms) result=%r",
                        tid,
                        qualname,
                        elapsed_ms,
                        result,
                    )
                else:
                    target_logger.log(
                        level,
                        "[trace=%s] EXIT %s (%.2fms)",
                        tid,
                        qualname,
                        elapsed_ms,
                    )
                return result

        if inspect.iscoroutinefunction(func):
            return async_wrapper  # type: ignore[return-value]
        return sync_wrapper  # type: ignore[return-value]

    return decorator