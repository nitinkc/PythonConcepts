from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Calculator:
    def add(self, *values: int | float) -> int | float:
        if not all(isinstance(value, (int, float)) for value in values):
            raise TypeError("all values must be numeric")
        return sum(values)

    def subtract(self, left: int | float, right: int | float) -> int | float:
        return left - right

    def multiply(self, left: int | float, right: int | float) -> int | float:
        return left * right


def main() -> None:
    calculator = Calculator()
    print(calculator.add(1, 2, 3))
    print(calculator.multiply(3, 4))


if __name__ == "__main__":
    main()
