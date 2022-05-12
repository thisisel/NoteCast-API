from pydantic import BaseModel

class PaginatorInfo(BaseModel):
    currentPage : int
    hasMorePages : bool
    total : int

