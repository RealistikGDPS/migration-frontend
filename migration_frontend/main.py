from __future__ import annotations

from databases import DatabaseURL
from quart import g
from quart import Quart
from quart import render_template
from quart import request

from migration_frontend import config
from migration_frontend.adapters.mysql import MySQLService
from migration_frontend.repository import Repository


async def render_page(
    path: str,
    title: str,
    **kwargs,
) -> str:
    # This might be a bit unsafe for social engineering but oh wellll.
    success = request.args.get("success")
    error = request.args.get("error")
    warning = request.args.get("warning")

    return await render_template(
        path,
        title=title,
        success=success,
        error=error,
        warning=warning,
        **kwargs,
    )


def repo() -> Repository:
    return Repository(g.sql)


def configure_routes(app: Quart) -> None:
    @app.route("/")
    async def main():
        user_count = await repo().get_member_count()

        return await render_page(
            "home.html",
            title="Home",
            user_count=user_count,
        )

    @app.route("/password/migrate", methods=["GET", "POST"])
    async def migrate_password():
        return await render_page(
            "tools/password_migrate.html",
            title="Migrate Password",
        )


def configure_mysql(app: Quart) -> None:
    mysql = MySQLService(
        DatabaseURL(
            f"mysql+asyncmy://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DATABASE}",
        ),
    )

    @app.before_request
    async def transaction_start():
        g.sql = await mysql.transaction().__aenter__()

    @app.after_request
    async def transaction_end(r):
        await g.sql.__aexit__()

        return r


def init_app() -> Quart:
    app = Quart(
        __name__,
        static_folder="../static",
        template_folder="../templates",
    )

    configure_mysql(app)
    configure_routes(app)

    return app


asgi_app = init_app()
