from fastapi import APIRouter
from typing import Tuple

from searcher.company.endpoints import router as company_router


def create_routers() -> Tuple[APIRouter, APIRouter]:
    api = APIRouter()
    view = APIRouter()

    router_configs = [
        (api, company_router, '', ["company"]),
    ]

    for p, c, prefix, tags in router_configs:
        p.include_router(c, prefix=prefix, tags=tags)

    return api, view
