"""FastAPI application factory."""

from fastapi import Depends, FastAPI

from tsnt import __version__
from tsnt.api.auth import require_api_key
from tsnt.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="TSNT Engine",
        version=__version__,
        description=(
            "Reproducible strategic-network scenario analysis. "
            "Outputs are conditional model results, not predictions of conflict."
        ),
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    app.include_router(router, dependencies=[Depends(require_api_key)])
    return app
