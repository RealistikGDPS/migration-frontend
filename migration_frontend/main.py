from __future__ import annotations

from quart import Quart


def init_app() -> Quart:
    app = Quart(__name__, static_folder="../static", template_folder="../templates")

    return app


asgi_app = init_app()
