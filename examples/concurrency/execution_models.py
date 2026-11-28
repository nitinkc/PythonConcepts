import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from time import sleep

def blocking_io(value: int) -> int:
    sleep(0.01)
    return value

def cpu_bound(value: int) -> int:
    return sum(number * number for number in range(value))

def run_threaded(values: list[int]) -> list[int]:
    with ThreadPoolExecutor() as executor:
        return list(executor.map(blocking_io, values))

def run_parallel(values: list[int]) -> list[int]:
    with ProcessPoolExecutor() as executor:
        return list(executor.map(cpu_bound, values))

async def run_async(values: list[int]) -> list[int]:
    async def identity(value: int) -> int:
        await asyncio.sleep(0.01)
        return value

    return list(await asyncio.gather(*(identity(value) for value in values)))

def main() -> None:
    values = [1, 2, 3]
    print(run_threaded(values))
    print(run_parallel(values))
    print(asyncio.run(run_async(values)))


if __name__ == "__main__":
    main()
