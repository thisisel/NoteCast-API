from tasks import (cpu_queue, get_current_job, get_first_dependent_result, job,
                hybrid_queue, redis_conn)




@job(cpu_queue)
def update_transcription(q_id, transcript=None):
    from note_cast.db.crud.quote import QuoteQuery

    if transcript is None:
        current_job = get_current_job(redis_conn)
        transcript = get_first_dependent_result(hybrid_queue, current_job)

    QuoteQuery.update_transcript(q_id=q_id, transcript=transcript)
