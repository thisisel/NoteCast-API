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
    users_in_db: List[User] = [User(**u_v).save() for u_v in users.values()]
    return users_in_db


podcasts = {
    "p1": {
        "p_id": "73209",
        "p_title": "Hidden Brain",
        "description": "Shankar Vedantam uses science and storytelling to reveal the unconscious patterns that drive human behavior, shape our choices and direct our relationships.",
        "web_url": "https:\/\/hidden-brain.simplecast.com",
        "image_url": "https:\/\/image.simplecastcdn.com\/images\/5b7d8c77-15ba-4eff-a999-2e725db21db5\/5da6be39-fd7a-4d15-80cb-9b518d140957\/3000x3000\/hidden-brain-cover.jpg?aid=rss_feed",
        "feed_url": "https:\/\/feeds.simplecast.com\/kwWc0lhf",
        "podchaser_url": "https:\/\/www.podchaser.com\/podcasts\/hidden-brain-73209",
        "_episodes": {
            "e1": {
                "e_id": "2515575",
                "e_title": "Encore of Episode 11: Forgery",
                "audio_url": "https:\/\/dts.podtrac.com\/redirect.mp3\/chrt.fm\/track\/21283G\/stitcher.simplecastaudio.com\/df179a36-a022-41e3-bf7c-b7a4efc6f51e\/episodes\/8a07f1e4-2c60-4f08-a37a-7209942844af\/audio\/128\/default.mp3?aid=rss_feed&awCollectionId=df179a36-a022-41e3-bf7c-b7a4efc6f51e&awEpisodeId=8a07f1e4-2c60-4f08-a37a-7209942844af&feed=kwWc0lhf",
                "length_s": 1403,
                "description": "This week on Hidden Brain, Shankar talks to Google's Laszlo Bock for insider tips and insights about what works — and what doesn't work — in recruiting, motivating, and retaining a talented workforce.\n",
                "air_date": "2016-08-16 04:04:00",
                "_quotes": {
                    "q1": {
                        "q_id": "3f5062e0-2f39-4d2c-aca5-d15b9d9c4918",
                        "transcript": "Praesentium placeat fuga praesentium distinctio dolores iste et ab.Odio quia rerum et ut.",
                        "mention_rel": {
                            "start_offset_h": 0,
                            "start_offset_m": 16,
                            "start_offset_s": 0,
                            "end_offset_h": 0,
                            "end_offset_m": 17,
                            "end_offset_s": 10,
                        },
                    },
                },
            },
            "e2": {
                "e_id": "2515594",
                "e_title": "Episode 34: Google at Work",
                "audio_url": "https:\/\/dts.podtrac.com\/redirect.mp3\/chrt.fm\/track\/21283G\/stitcher.simplecastaudio.com\/df179a36-a022-41e3-bf7c-b7a4efc6f51e\/episodes\/9f29af7f-3f6d-4223-aea1-89f8f1f70119\/audio\/128\/default.mp3?aid=rss_feed&awCollectionId=df179a36-a022-41e3-bf7c-b7a4efc6f51e&awEpisodeId=9f29af7f-3f6d-4223-aea1-89f8f1f70119&feed=kwWc0lhf",
                "length_s": 1596,
                "description": "This week on Hidden Brain, Shankar talks to Google's Laszlo Bock for insider tips and insights about what works — and what doesn't work — in recruiting, motivating, and retaining a talented workforce.\n",
                "air_date": "2016-06-07 04:00:00",
                "_quotes": {
                    "q1": {
                        "q_id": "a87b5a93-e989-4666-bc05-acb4a1072e71",
                        "transcript": "Et dolorem dolorum repudiandae qui dolorem velit.Temporibus cum iste molestiae voluptatibus occaecati adipisci odit neque.",
                        "mention_rel": {
                            "start_offset_h": 0,
                            "start_offset_m": 6,
                            "start_offset_s": 30,
                            "end_offset_h": 0,
                            "end_offset_m": 7,
                            "end_offset_s": 30,
                        },
                    },
                    "q2": {
                        "q_id": "222f127c-e32d-408e-b436-e7a7c6d33859",
                        "transcript": "Dolores odit earum eius cum deserunt. Odio omnis illo id recusandae ea corrupti qui. Velit tempore at aliquam. Quia nulla qui autem perspiciatis est qui ipsam ipsa nulla.",
                        "mention_rel": {
                            "start_offset_h": 0,
                            "start_offset_m": 25,
                            "start_offset_s": 40,
                            "end_offset_h": 0,
                            "end_offset_m": 27,
                            "end_offset_s": 0,
                        },
                    },
                },
            },
        },
    },
    "p2": {
        "p_id": "27717",
        "p_title": "Myths and Legends",
        "description": "Jason Weiser tells stories from myths, legends, and folklore that have shaped cultures throughout history. Some, like the stories of Aladdin, King Arthur, and Hercules are stories you think you know, but with surprising origins. Others are stories you might not have heard, but really should. All the stories are sourced from world folklore, but retold for modern ears. These are stories of wizards, knights, Vikings, dragons, princesses, and kings from the time when the world beyond the map was a dangerous and wonderful place. ",
        "web_url": "https:\/\/www.mythpodcast.com",
        "image_url": "https:\/\/www.podchaser.com\/podcasts\/myths-and-legends-27717",
        "feed_url": "https:\/\/www.omnycontent.com\/d\/playlist\/9b7dacdf-a925-4f95-84dc-ac46003451ff\/662ff2d4-9b7f-4388-8a94-acb8002fd595\/480aa1a5-4ada-4846-ae18-acb8002fd59e\/podcast.rss",
        "podchaser_url": "https:\/\/www.podchaser.com\/podcasts\/myths-and-legends-27717",
        "_episodes": {
            "e1": {
                "e_id": "3209534",
                "e_title": "37-Hercules: The Best at What He Does",
                "audio_url": "https:\/\/arttrk.com\/p\/KSTA5\/chrt.fm\/track\/B7AB5D\/pdst.fm\/e\/dts.podtrac.com\/redirect.mp3\/traffic.omny.fm\/d\/clips\/9b7dacdf-a925-4f95-84dc-ac46003451ff\/662ff2d4-9b7f-4388-8a94-acb8002fd595\/a2f72d19-9af4-431d-93a5-acb800605c49\/audio.mp3?utm_source=Podcast&in_playlist=480aa1a5-4ada-4846-ae18-acb8002fd59e",
                "image_url": "https:\/\/www.omnycontent.com\/d\/clips\/9b7dacdf-a925-4f95-84dc-ac46003451ff\/662ff2d4-9b7f-4388-8a94-acb8002fd595\/a2f72d19-9af4-431d-93a5-acb800605c49\/image.jpg?t=1611294653&size=Large",
                "length_s": 2705,
                "description": 'Hercules is as terrible as he is awesome. There are sea monsters, centaurs, people being thrown off of things, Hydra poison, and Hercules making ridiculous choices. Basically, it\'s everything you could want from a Hercules episode. Oh, and he dies, because apparently he can do that. The creature this time is the Mamagwasewug, and he just wants to borrow a smoke off you...or he\'ll burn your house down.   Batman picture: https:\/\/www.instagram.com\/p\/BHD5g9OjfXq\/?taken-by=mythpodcast Our sponsor this week: www.lootcrate.com\/legends (code: LEGENDS).  Support the show? (http:\/\/support.mythpodcast.com) Find us on iTunes? (http:\/\/itunes.mythpodcast.com) Music:  "Cheap suit" by Jason Staczek  "Silence" by Kai Engel  "Deserted City" by Kai Engel  "At the End Everyone Dies" by Kai Engel  "Leafless Quince Tree" by Rolemusic All other music by Poddington Bear and Blue Dot Sessions. Bibliography: "Metamorphoses" by Ovid 9:1-282 "The Women of Trachis" by Sophocles "The Library of Greek Mythology" by Apollodorus 2:6-8 "Library of History" by Diodorus Siculus 4:32 "The Greek Myths" by Robert Graves\n\nSee omnystudio.com\/listener for privacy information.',
                "air_date": "2016-06-29 03:59:00",
                "_quotes": {
                    "q1": {
                        "q_id": "627bbaaf-9bed-4037-8b18-9948cd6efa65",
                        "transcript": "Cumque excepturi maxime esse qui culpa vitae veniam aliquid eos. Provident porro explicabo nulla. Expedita quaerat aperiam laudantium asperiores. Maiores aperiam amet laudantium. Atque quidem dignissimos sunt suscipit voluptas voluptatem blanditiis aspernatur.",
                        "mention_rel": {
                            "start_offset_h": 0,
                            "start_offset_m": 10,
                            "start_offset_s": 20,
                            "end_offset_h": 0,
                            "end_offset_m": 12,
                            "end_offset_s": 0,
                        },
                    },
                },
            },
            "e2": {
                "e_id": "3209585",
                "e_title": "23-Cupid and Psyche: Burned",
                "audio_url": "https:\/\/arttrk.com\/p\/KSTA5\/chrt.fm\/track\/B7AB5D\/pdst.fm\/e\/dts.podtrac.com\/redirect.mp3\/traffic.omny.fm\/d\/clips\/9b7dacdf-a925-4f95-84dc-ac46003451ff\/662ff2d4-9b7f-4388-8a94-acb8002fd595\/9395b5aa-af99-4825-bf7f-acb80061dbfe\/audio.mp3?utm_source=Podcast&in_playlist=480aa1a5-4ada-4846-ae18-acb8002fd59e",
                "image_url": "https:\/\/www.omnycontent.com\/d\/clips\/9b7dacdf-a925-4f95-84dc-ac46003451ff\/662ff2d4-9b7f-4388-8a94-acb8002fd595\/9395b5aa-af99-4825-bf7f-acb80061dbfe\/image.jpg?t=1611294980&size=Large",
                "length_s": 2231,
                "description": 'In this famous story from Greek Mythology, we\'ll meet Cupid (not a baby), as he accidentally nicks himself with his own arrow. In a podcast episode that is  like the movie "Mean Girls" with a trip to the Greek underworld, you\'ll see why it is against the law to harbor someone who\'s prettier than a goddess.\nThe creature of the week is a forest creature that operates on a very annoying wood chip economy.\nBecome a member\nSay Hi on Twitter\nFind the show on iTunes\nThe bag of dirt\nMusic:\n"Sonar Despierto" by Zifhang\n"Sidecar" by Podington Bear\n"The Vault" by Trigg & Gusset\n"The Coil Winds" by Blue Dot Sessions\n"Transmogrify" by Podington Bear\n"Here is Now" by Ketsa\n"Trellis" by Podington Bear\n\nSee omnystudio.com\/listener for privacy information.',
                "air_date": "2016-02-17 04:59:32",
                "_quotes": {
                    "q1": {
                        "q_id": "c411174c-ab36-47a4-a644-5cce193d03de",
                        "transcript": "Soluta recusandae dolores rerum. Et ut adipisci perferendis dolores ex et voluptatem. Suscipit et velit tenetur sunt iure dolores ratione eveniet. Et consequatur voluptates quia distinctio modi cum quia.",
                        "mention_rel": {
                            "start_offset_h": 0,
                            "start_offset_m": 24,
                            "start_offset_s": 0,
                            "end_offset_h": 0,
                            "end_offset_m": 25,
                            "end_offset_s": 10,
                        },
                    },
                    "q2": {
                        "q_id": "d5155279-0d20-423c-ad03-073a5445b133",
                        "transcript": "Rerum sunt qui officia delectus voluptates et temporibus sunt. Reprehenderit optio consequuntur vero vel et doloremque aut. Ut quasi magni.",
                        "mention_rel": {
                            "start_offset_h": 0,
                            "start_offset_m": 11,
                            "start_offset_s": 15,
                            "end_offset_h": 0,
                            "end_offset_m": 12,
                            "end_offset_s": 45,
                        },
                    },
                },
            },
        },
    },
}


def seed_podcast_items(podcasts : dict):
    p_db_list = []
    e_db_list = []
    q_db_list = []

    for p_v in podcasts.values():
        p_db = Podcast(**p_v).save()

        episodes: dict = p_v.get("_episodes")
        for e_v in episodes.values():
           e_db = Episode(**e_v).save()
           
           quotes : dict = e_v.get("_quotes")
           for q_v in quotes.values():
               q_db = Quote(**q_v).save()
               
               q_db.mentioned_on.connect(e_db, q_v.get("mention_rel"))
               q_db_list.append(q_db)
            
           e_db.published_for.connect(p_db, {"date": e_v.get("air_date")})
           e_db_list.append(e_db)

        p_db_list.append(p_db)

    return p_db_list, e_db_list, q_db_list


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
    seed_podcast_items(podcasts=podcasts)
