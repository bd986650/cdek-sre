from fastapi import FastAPI, Request, Response
import time

app = FastAPI()

request_count = 0
error_count = 0
request_latency_sum = 0.0
request_latency_count = 0


@app.get("/")
async def root():
    global request_count
    request_count += 1
    return Response(content="OK", media_type="text/plain")


@app.get("/metrics")
async def metrics():
    global request_count
    request_count += 1
    body = (
        "# HELP http_requests_total Total requests\n"
        "# TYPE http_requests_total counter\n"
        f"http_requests_total {request_count}\n"
        "# HELP http_errors_total Total errors\n"
        "# TYPE http_errors_total counter\n"
        f"http_errors_total {error_count}\n"
    )
    return Response(content=body, media_type="text/plain")


@app.middleware("http")
async def track_errors(request: Request, call_next):
    global error_count, request_latency_sum, request_latency_count
    start = time.monotonic()
    try:
        response = await call_next(request)
        if response.status_code >= 500:
            error_count += 1
        return response
    except Exception:
        error_count += 1
        raise
    finally:
        duration = time.monotonic() - start
        request_latency_sum += duration
        request_latency_count += 1
