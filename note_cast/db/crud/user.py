from neomodel import Q
from note_cast.security.login_manager import manager as login_manager

from ..models import User


@login_manager.user_loader()
def load_user(user_id: str):
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

        for key, val in q.items():
            try:
                if val is not None:
                    return User.nodes.filter(q[key])[0]
            except IndexError:
                return None

    @staticmethod
    def find_user_notes_all(user: User):
        # if (user := User.nodes.get_or_none(u_id=u_id)) is not None:
        #     return user.notes
        # # raise user not found ex 404
        # return {'error':'user not found 404'}
        return user.notes
