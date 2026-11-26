## 🔑 FastAPI One-Page Cheat Sheet

```python
from fastapi import FastAPI, HTTPException, Depends, Query, Path, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

app = FastAPI()

# CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# Pydantic model
class Item(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    tags: List[str] = []


# Dependency
def get_db():
    db = connect()
    try:
        yield db
    finally:
        db.close()


# Routes
@app.get("/items/", response_model=List[Item])
@app.get("/items/{id}", response_model=Item)
@app.post("/items/", response_model=Item, status_code=201)
@app.put("/items/{id}", response_model=Item)
@app.patch("/items/{id}", response_model=Item)
@app.delete("/items/{id}", status_code=204)

# Key patterns
# raise HTTPException(status_code=404, detail="Not found")
# item.model_dump(exclude_unset=True)  ← for PATCH
# background_tasks.add_task(fn, arg)
# Depends(get_db), Depends(get_current_user)
```

## Project settings
- [project.scripts] - Console script - runs `__init__.py`
- [tool.fastapi] entrypoint in pyproject.toml- runs `main.py`


**Use `fastapi dev `to run the API**: Keep `uv run fastapi dev ... --port 8001 `

(or uv run fastapi run ... --port 8001 for non-reload mode) for serving the FastAPI app,
and reserve [project.scripts] for **custom CLI tasks** or scripts you explicitly want to run.