import logging
from itertools import count
from time import perf_counter

from api.routers.category import category_router
from api.routers.tasks import task_router
from core.config import get_settings
from core.loging import configure_logging
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(task_router)
app.include_router(category_router)

settings = get_settings()

configure_logging()
logger = logging.getLogger("app.midleware")

request_counter = count(1)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.middleware(
    "http"
)  # log_requests выполнится до и после обработки каждого HTTP-запроса
async def log_requests(request: Request, call_next) -> Response:
    started_at = perf_counter()
    request_number = next(request_counter)
    try:
        response: Response = await call_next(request)  # Работа самого эндпоинта
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    response.headers["X-Request-Number"] = str(request_number)
    return response


# START ROOT
@app.get("/")
def read_root():
    return {"message": "Hello world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", port=8080, reload=True)
