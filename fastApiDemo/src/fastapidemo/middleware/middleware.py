import time
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from fastapidemo.decorators.logger import set_trace_id
from fastapidemo.main import app

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)  # call the actual route handler
    process_time = time.time() - start
    response.headers["X-Process-Time"] = str(process_time)
    # Custom response header
    response.headers["Nitin-Response-Header"] = "Happy Thanksgiving Nov 26, 26"

    ############ Decorator Demo ###########
    incoming_id = incoming_id = request.headers.get("X-Trace-ID")
    tid = set_trace_id(incoming_id)
    response.headers["X-Trace-ID"] = tid
    ########### Decorator demo ends ###########
    return response

app.add_middleware(
    CORSMiddleware,
    # For UI Client
    allow_origins=["https://myapp.com", "http://localhost:3000"],  # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)