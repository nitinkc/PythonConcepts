from functools import wraps

def trace_name(function):
    @wraps(function) # A decorator from Python's built-in functools module (from functools import wraps)
    def wrapper(*args, **kwargs):
        print(f"Decorator Demo: %s" % function.__name__) # Runs before the original function is invoked, printing the wrapped function's original name.
        return function(*args, **kwargs)

    return wrapper

@trace_name
def multiply(a: int, b: int) -> int:
    return a * b

print(multiply(2, 3))