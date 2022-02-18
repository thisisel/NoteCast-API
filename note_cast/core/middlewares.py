from fastapi import Request
from fastapi.exceptions import HTTPException

async def catch_Permissionerror_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except PermissionError:
        # you probably want some kind of logging here
        # return Response("Internal server error", status_code=500)
        raise HTTPException(401)