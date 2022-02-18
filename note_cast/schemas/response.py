from pydantic import BaseModel


class ApiBaseResponse(BaseModel):
    status: bool
    message: str


# TODO Document example for 500 and 404
class ApiErrorResponse(BaseModel):
    status: bool = False
    category: str
    message: Optional[str]