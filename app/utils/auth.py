from fastapi import HTTPException
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param


class HTTPAuthorizationHeader(SecurityBase):
    def __init__(self, authorization: str = None):
        self.authorization = authorization

    def __call__(self, api_key: str = None):
        if api_key:
            self.authorization = api_key
        if not self.authorization:
            raise HTTPException(
                status_code=401,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        scheme, credentials = get_authorization_scheme_param(self.authorization)
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return credentials

    @property
    def credentials(self):
        return self()

    def is_expired(self):
        pass
