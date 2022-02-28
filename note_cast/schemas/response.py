from typing import Optional
from pydantic import BaseModel
from . user import UserPydantic, BaseUserPydantic

class ApiBaseResponse(BaseModel):
    status: bool
    message: str

class CloudinarySuccessResponse(ApiBaseResponse):
    detail : Optional[dict]
    asset_public_id : Optional[str]

# TODO Document example for 500 and 404
class ApiErrorResponse(BaseModel):
    status: bool = False
    category: str
    message: Optional[str]

class RestRegisterSuccessResp(ApiBaseResponse):
    user : UserPydantic

class RestLoginSuccessResp(ApiBaseResponse):
    user : BaseUserPydantic
    token : str
