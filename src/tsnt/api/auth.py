"""Optional API-key protection for production deployments."""

import secrets
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from tsnt.config import Settings, get_settings


def require_api_key(
    supplied: Annotated[str | None, Header(alias="X-API-Key")] = None,
    settings: Settings = Depends(get_settings),
) -> None:
    if settings.api_key and (
        supplied is None or not secrets.compare_digest(supplied, settings.api_key)
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid API key")
