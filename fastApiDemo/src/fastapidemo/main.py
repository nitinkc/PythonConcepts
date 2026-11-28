import logging

from fastapi import FastAPI

from fastapidemo.events.lifeCycleEvents import lifespan
from fastapidemo.models.model import ModelName

# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s %(levelname)s %(name)s - %(message)s",
# )

app = FastAPI(lifespan=lifespan)

# These modules do `from fastapidemo.main import app` and register exception
# handlers / middleware on it as an import side effect, so they must be
# imported only after `app` exists.
from fastapidemo.middleware import middleware  # noqa: E402, F401
from fastapidemo.exception import customException  # noqa: E402, F401
from fastapidemo.routers import orders, products, users  # noqa: E402

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/status")
def read_root():
    return {"status": "ok"}

@app.get("/models/{llm_model_name}")
def get_model(llm_model_name: ModelName) : #  ←  type hint for Enum
    if llm_model_name == ModelName.alexnet:
        return {"model": llm_model_name, "message": "Deep Learning FTW!"}
    return {"model": llm_model_name}

app.include_router(products.router)
app.include_router(users.router)
app.include_router(orders.router, prefix="/v2")  # Override/extend prefix
