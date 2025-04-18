import multiprocessing
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

import bas_processor.common.globals as bas_globals

from bas_processor.api.router import router
from bas_processor.db.models import Base
from bas_processor.db.session import engine

from utils.bas_utils.async_service_app import run_async_service
from utils.ut_logging import LOGGING_SECTION

SERVICE_NAME = "bas_processor"


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    raise SystemExit()


async def main(config: dict):
    bas_globals.init_service_config(config)
    bas_globals.init_service_logger(SERVICE_NAME, config)

    global app
    app = FastAPI(title=SERVICE_NAME, lifespan=lifespan)
    app.include_router(router, prefix="/api")

    config_uvicorn = uvicorn.Config(app=app,
                                    host="0.0.0.0",
                                    port=8080,
                                    log_config=config[LOGGING_SECTION])

    await uvicorn.Server(config_uvicorn).serve()


async def on_stop_callback():
    pass
    # bas_globals.resource_manager.stop()
    # await bas_globals.stop_subscribers()


if __name__ == "__main__":
    os.environ["no_proxy"] = "*"
    multiprocessing.set_start_method('fork', True)
    run_async_service(service_name=SERVICE_NAME,
                      main_coro=main,
                      on_stop=on_stop_callback())
