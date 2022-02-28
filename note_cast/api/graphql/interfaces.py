import strawberry


@strawberry.interface
class IUser:
    u_id: strawberry.ID
    username: str
    email: str

@strawberry.interface
class IGQResponse:
    status: bool
    message: str