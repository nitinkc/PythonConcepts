from contextlib import asynccontextmanager
from fastapi import FastAPI

# Modern approach
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: runs before the app starts serving requests
    print("LIFESPAN : ############ Starting up... ############")

    yield  # ← app runs here

    # SHUTDOWN: runs when the app is stopping
    print("LIFESPAN : ############ Shutting down... ############")