from .. models import Podcast, Category, Episode, Quote, Note, User

def create_sample_data():
    hidden_brain: Podcast = Podcast(p_id="1", title="Hidden Brain").save()
    psychology: Category = Category(name="Psychology").save()

    hidden_brain.category.connect(psychology)

    julie_ort_story_description = """Julie is having a very bad day.
                                     She’s hiding out in the library when a stranger 
                                     offers a comforting gift."""
    julie_ort_story: Episode = Episode(
        title="julie ort",
        length_h=0,
        length_m=5,
        length_s=54,
        num=200,
        description=julie_ort_story_description,
    ).save()

    julie_ort_story.published_for.connect(hidden_brain)

    julie_quote: Quote = Quote(
        text="I don't remember your name, I have forgoten your face, but I will never forget your kindess"
    ).save()

    julie_quote.mentioned_on.connect(
        julie_ort_story,
        {
            "start_time_h": 0,
            "start_time_m": 1,
            "start_time_s": 18,
            "end_time_h": 0,
            "end_time_m": 1,
            "end_time_s": 26,
        },
    )

    elahe: User = User(
        username="thisisel", email="1997.esm@gmail.com", password_hash="ljji123++@"
    ).save()
    note_elahe_juli: Note = Note(text="You reap what you had sown").save()

    # note_elahe_juli.author.connect(elahe, {'date' : datetime(2018, 6, 1)})
    note_elahe_juli.author.connect(elahe)
    note_elahe_juli.attach_to.connect(julie_quote)
    note_data = {
        'text' : "You reap what you had sown",
    }
    # elahe.notes.connect(julie_quote, note_data)