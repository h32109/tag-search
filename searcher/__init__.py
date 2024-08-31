from contextlib import asynccontextmanager

from fastapi import FastAPI

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from searcher.core.config import settings
from searcher.db.ctx import SQLContext
from searcher.middleware import DBSessionMiddleware
from searcher.models import get_models
from searcher.routes import create_routers
from searcher.service import Service


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_context()
    await setup_service_manager(settings)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        version=settings.APP_VERSION,
        docs_url="/docs" if settings.is_dev else None,
        lifespan=lifespan
    )
    setup_context(settings)
    setup_routers(app)
    setup_middlewares(app)

    return app


def setup_routers(app: FastAPI):
    api_router, view_router = create_routers()
    app.include_router(api_router)
    app.include_router(view_router)


def setup_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    from searcher.globals import sql
    app.add_middleware(
        DBSessionMiddleware,
        run_session=sql.run_session
    )


async def setup_service_manager(settings):
    await Service.init(settings)


def setup_context(settings):
    SQLContext.init(
        settings=settings,
        models=get_models(),
        session_maker_args={"class_": AsyncSession})


async def start_context():
    from searcher.globals import sql
    await sql.start()
