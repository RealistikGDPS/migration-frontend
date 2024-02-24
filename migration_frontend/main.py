from __future__ import annotations

from quart import Quart
from quart import render_template


def configure_routes(app: Quart) -> None:
    @app.route("/")
    async def main():
        return await render_template(
            "home.html",
            title="Home",
        )


def init_app() -> Quart:
    app = Quart(
        __name__,
        static_folder="../static",
        template_folder="../templates",
    )

    configure_routes(app)

    return app


asgi_app = init_app()
