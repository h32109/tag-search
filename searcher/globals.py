from functools import partial
from werkzeug import local

from sqlalchemy.ext.declarative import declarative_base

from searcher.db.base import Context

Base = declarative_base()


def lookup_context(ctx: Context, name: str | None = None):
    if name is None:
        return ctx.get()
    return getattr(ctx, name, ctx).get(name)


sql = local.LocalProxy(
    partial(
        lookup_context,
        Context,
        "sql")
)
