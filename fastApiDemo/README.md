
```shell
uv init fastApiDemo\n
cd fastApiDemo
uv add "fastapi[standard]"

# Add into project.toml
#[tool.fastapi]
#entrypoint = "fastApiDemo.main:app"
uv run fastApiDemo dev --port 8001\n
```

## Issues :
0. We have a code in the __init__.py and main.py, which one runs and when and when its useful
1. Fix the Exception thrown if more than 10 quantity  of a product is attempted to be ordered
2. Locate the response header where Happy Thanksgiving is sent with every response
3. Implement the delete functionality (with fake DB)
4. 