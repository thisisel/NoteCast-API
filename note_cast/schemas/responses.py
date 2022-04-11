from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

from pydantic import BaseModel

# if TYPE_CHECKING:
#     from .user import BaseUserPydantic, UserPydantic
from .user import BaseUserPydantic, UserPydantic

class ApiBaseResponse(BaseModel):
    timestamp: datetime = datetime.utcnow()
    message: str
    data: Optional[Union[dict, List[dict], BaseModel, List[BaseModel]]] = None
    status: bool = True


class CloudinarySuccessResponse(ApiBaseResponse):
    asset_public_id: Optional[str]


class ApiErrorResponse(BaseModel):
    timestamp: datetime = datetime.utcnow()
    status_code: Optional[int] = None
    detail: Optional[str] = None
    status: bool = False
    category: Optional[str] = None
    errors: Any = None


class RestRegisterSuccessResp(ApiBaseResponse):
    user: UserPydantic


class RestLoginSuccessResp(ApiBaseResponse):
    user: BaseUserPydantic
    access_token: str
    token_type: str = "Bearer"


class PageResponse(ApiBaseResponse):
    skip: int = 0
    limit: int = 0
