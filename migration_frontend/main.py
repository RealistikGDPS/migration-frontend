from __future__ import annotations

import sys

from databases import DatabaseURL
from quart import g
from quart import Quart
from quart import redirect
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

    @app.route("/error")
    async def error():
        return await render_page(
            "errors/exception.html",
            "Server Error",
        )

    @app.route("/not-found")
    async def not_found():
        return await render_page("errors/not_found.html", "Page Not Found")


def configure_mysql(app: Quart) -> None:
    @app.before_serving
    async def on_start():
        mysql = MySQLService(
            DatabaseURL(
                f"mysql+asyncmy://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DATABASE}",
            ),
        )
        await mysql.connect()
        g.pool = mysql

    @app.before_request
    async def transaction_start():
        g.sql = await g.pool.transaction().__aenter__()

    @app.after_request
    async def transaction_end(r):
        await g.sql.__aexit__(None, None, None)

        return r

    @app.errorhandler(500)
    async def exception_handler(_):
        exc = sys.exc_info()

        await g.sql.__aexit__(*exc)

        return redirect("/error")


def configure_errors(app: Quart) -> None:
    @app.errorhandler(404)
    async def not_found(_):
        return redirect("/not-found")


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
