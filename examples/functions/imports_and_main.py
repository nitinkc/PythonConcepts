def describe_execution(module_name: str) -> str:
    if module_name == "__main__":
        return "The module is running as the program entry point."
    return f"The module was imported as {module_name}."


def main() -> None:
    print(describe_execution(__name__))


if __name__ == "__main__":
    main()
