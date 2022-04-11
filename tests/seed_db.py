from typing import List
from note_cast.db.models import User, Podcast, Episode, Quote, Note

users = {
    "u_1": {
        "username": "Felipa30",
        "email": "Gerry55@yahoo.com",
        "password": "XZIjXsVFPQwEkYS",
    },
    "u_2": {
        "username": "Prince.Rosenbaum75",
        "email": "Lawson.Vandervort18@gmail.com",
        "password": "1KuGLU3uKmVd7Df",
    },
    "u_3": {
        "username": "Wendy.Bernier",
        "email": "Marie53@yahoo.com",
        "password": "DP9tjrCuCYO4YKr",
    },
    "u_4": {
        "username": "sandman_enters",
        "email": "Brenda_OConner@yahoo.com",
        "password": "nJ3TKroFtyo0lsi",
    },
    "u_5": {
        "username": "Elliot.Schiller",
        "email": "Deborah_Luettgen@hotmail.com",
        "password": "LMRGt15q8mdCV_E",
    },
    "u_6": {
        "username": "Queen_Conroy16",
        "email": "Asa32@gmail.com",
        "password": "h97IDTVnExYfcxD",
    },
}


def seed_users(users: dict) -> List[User]:
    users_in_db: List[User] = [User(**u).save() for u in users]
    return users_in_db


podcasts = {
    "p1": {
        "p_id": "",
        "p_title": "",
        "description": "",
        "_episodes": {
            "e1": {
                "e_id": "",
                "e_title": "",
                "audio_url": "",
                "length_s": "",
                "description": "",
                "air_date": "",
                "quotes": {
                    "q1": {
                        "q_id": "",
                        "transcript": "",
                        "mention_rel": {
                            "start_offset_h": "",
                            "start_offset_m": "",
                            "start_offset_s": "",
                            "end_offset_h": "",
                            "end_offset_m": "",
                            "end_offset_s": "",
                        },
                    },
                },
            },
            "e2": {
                "e_id": "",
                "e_title": "",
                "audio_url": "",
                "length_s": "",
                "description": "",
                "air_date": "",
                "quotes": {
                    "q1": {
                        "q_id": "",
                        "transcript": "",
                        "mention_rel": {
                            "start_offset_h": "",
                            "start_offset_m": "",
                            "start_offset_s": "",
                            "end_offset_h": "",
                            "end_offset_m": "",
                            "end_offset_s": "",
                        },
                    },
                    "q2": {
                        "q_id": "",
                        "transcript": "",
                        "mention_rel": {
                            "start_offset_h": "",
                            "start_offset_m": "",
                            "start_offset_s": "",
                            "end_offset_h": "",
                            "end_offset_m": "",
                            "end_offset_s": "",
                        },
                    },
                },
            },
        },
    },
    "p2": {
        "p_id": "",
        "p_title": "",
        "description": "",
        "_episodes": {
            "e1": {
                "e_id": "",
                "e_title": "",
                "audio_url": "",
                "length_s": "",
                "description": "",
                "air_date": "",
                "quotes": {
                    "q1": {
                        "q_id": "",
                        "transcript": "",
                        "mention_rel": {
                            "start_offset_h": "",
                            "start_offset_m": "",
                            "start_offset_s": "",
                            "end_offset_h": "",
                            "end_offset_m": "",
                            "end_offset_s": "",
                        },
                    },
                },
            },
            "e2": {
                "e_id": "",
                "e_title": "",
                "audio_url": "",
                "length_s": "",
                "description": "",
                "air_date": "",
                "quotes": {
                    "q1": {
                        "q_id": "",
                        "transcript": "",
                        "mention_rel": {
                            "start_offset_h": "",
                            "start_offset_m": "",
                            "start_offset_s": "",
                            "end_offset_h": "",
                            "end_offset_m": "",
                            "end_offset_s": "",
                        },
                    },
                    "q2": {
                        "q_id": "",
                        "transcript": "",
                        "mention_rel": {
                            "start_offset_h": "",
                            "start_offset_m": "",
                            "start_offset_s": "",
                            "end_offset_h": "",
                            "end_offset_m": "",
                            "end_offset_s": "",
                        },
                    },
                },
            },
        },
    },
}


def seed_podcasts():
    pass

# def seed_db():

#     u_1 : User = User(username="Wendy.Bernier", email="Gerry55@yahoo.com", password="XZIjXsVFPQwEkYS").save()
#     u_2 : User = User(username="sandman_enters", email="Lawson.Vandervort18@gmail.com", password="DP9tjrCuCYO4YKr").save()
#     u_3 : User = User(username="Elliot.Schiller", email="Marie53@yahoo.com", password="1KuGLU3uKmVd7Df").save()
#     u_4 : User = User(username="Queen_Conroy16", email="Brenda_OConner@yahoo.com", password="nJ3TKroFtyo0lsi").save()
#     u_5 : User = User(username="Felipa30", email="Deborah_Luettgen@hotmail.com", password="LMRGt15q8mdCV_E").save()
#     u_6 : User = User(username="Prince.Rosenbaum75", email="Asa32@gmail.com", password="h97IDTVnExYfcxD").save()

#     p_1 : Podcast = Podcast().save()
#     p_1_e1 : Episode = Episode().save()
#     #connect

#     p_1_e1_q1 : Quote = Quote().save()
#     #connect
#     p_1_e1_q2 : Quote = Quote().save()
#     #connect
#     p_1_e1_q3 : Quote = Quote().save()
#     #connect


#     p_1_e2 : Episode = Episode().save()
#     p_1_e3 : Episode = Episode().save()

if __name__ == "__main__":
    seed_users(users=users)
