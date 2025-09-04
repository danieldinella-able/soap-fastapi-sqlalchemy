"""Dipendenza FastAPI per autenticazione basata su token custom.

Header atteso: `Authorization: Token <valore>`.
Valida il token e restituisce il profilo utente associato, altrimenti 401.
"""

from fastapi import Header, HTTPException

from app.services.user_service import UserService


async def get_auth_profile(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Token "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization[len("Token "):].strip()
    success = await UserService().validate_auth_token(token)
    if not success:
        raise HTTPException(status_code=401, detail="Invalid token")

    profile = await UserService().get_profile_by_token(token)
    return profile
