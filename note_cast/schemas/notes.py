from pydantic import BaseModel, Field
from . user import BaseUserPydantic


# class BaseNote(BaseModel):
#     n_id : str
#     text : str = Field(..., min_length=50, max_length=450)
#     author : BaseUserPydantic = Field(...)
#     q_id : str


# class Note(BaseNote):
#     is_public : bool = True



####
class CreateNote(BaseModel):
    text : str = Field(..., min_length=50, max_length=450)
    q_id : str
    is_public : bool = True


class BaseNote(CreateNote):
    n_id : str
    author : BaseUserPydantic = Field(...)

class Note(BaseNote):
    is_public : bool = True