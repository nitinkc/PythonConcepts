
```shell
uv init fastApiDemo\n
cd fastApiDemo
uv add "fastapi[standard]"

# Add into project.toml
#[tool.fastapi]
#entrypoint = "fastApiDemo.main:app"
uv run fastApiDemo dev --port 8001
```

## Issues :
0. We have a code in the __init__.py and main.py, which one runs and when and when its useful
1. Fix the Exception thrown if more than 10 quantity  of a product is attempted to be ordered

### Response Header
2. Locate the response header where Happy Thanksgiving is sent with every response
3. Add a Trace id in each response : If i write a trace decorator with FastAPI, can i use it outside any framework. How to write a decorator
7. When a decorator is custom written, does it need to be registered in the request
   8. Requirement is to include trace for every response header

3. Move the middleware.py from root folder to middleware module and debug the issue.

3. Implement the delete functionality (with fake DB)
4. Background tasks not added (add one)
5. Authentication and Dependency Injection


