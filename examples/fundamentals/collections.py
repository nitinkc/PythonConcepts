def merge_profiles(defaults: dict, overrides: dict) -> dict:
    return defaults | overrides

def unique_in_order(values: list) -> list:
    return list(dict.fromkeys(values))

def main() -> None:
    defaults = {"theme": "light", "language": "en"}
    overrides = {"theme": "dark"}
    print(merge_profiles(defaults, overrides))
    print(unique_in_order(["python", "api", "python"]))

if __name__ == "__main__":
    main()
