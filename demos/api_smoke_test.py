import json
import os
import sys
from urllib import error, request

DEFAULT_BASE_URL = "http://127.0.0.1:8000"


def fetch_json(base_url: str, path: str):
    url = f"{base_url}{path}"
    with request.urlopen(url, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    base_url = os.getenv("API_BASE_URL", DEFAULT_BASE_URL)
    if len(sys.argv) > 1:
        base_url = sys.argv[1]

    expected = {
        "/": {"message": "Hello World"},
        "/health": {"status": "ok"},
    }

    for path, expected_body in expected.items():
        try:
            body = fetch_json(base_url, path)
        except error.URLError as exc:
            print(f"FAIL {path}: could not reach API at {base_url} ({exc})")
            return 1

        if body != expected_body:
            print(f"FAIL {path}: expected {expected_body}, got {body}")
            return 1

        print(f"PASS {path}: {body}")

    print("API smoke test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())


