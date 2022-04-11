from typing import List, Union

from neomodel import Q
from note_cast.security.login_manager import manager as login_manager

from ..models import Note, Quote, User


@login_manager.user_loader()
def load_user(user_id: str) -> Union[None, User]:
    """
    Get a user from the db
    :param user_id: E-Mail of the user
    :return: None or the user object
    """
    return User.nodes.get_or_none(email=user_id)


class QueryUser:
    @staticmethod
    def find_user(username: str = None, email: str = None, u_id: str = None):
        q = dict(
            username=Q(username=username),
            email=Q(email=email),
            u_id=Q(u_id=u_id),
        )
        mask = {"username": username, "email": email, "u_id": u_id}

        for key, val in mask.items():
            if val is not None:
                return User.nodes.get_or_none(q.get(key))

    @staticmethod
    def find_user_notes_all(
        user: User, skip: int = None, limit: int = None
    ) -> List[Note]:
        return user.notes.all()

    @classmethod
    def get_user_bookmarks(
        cls, user: User, skip: int = None, limit: int = None, **kwargs
    ) -> List[Quote]:
        user.bookmarks.all()

    @classmethod
    def add_bookmark(cls, user: User, quote: Quote):
        user.bookmarks.connect(quote)

    @classmethod
    def delete_bookmark(cls, q_id: str, user: User) -> Quote:
        if (bookmarked_quote := user.bookmarks.get_or_none()) is not None:
            user.disconnect(bookmarked_quote)
            return bookmarked_quote
        else:
            return None
