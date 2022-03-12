from tasks import (
    job,
    hybrid_queue,
    network_queue,
    get_first_dependent_result,
    get_current_job,
    redis_conn,
)

@job(hybrid_queue)
def fetch_transcription_flow(content=None):
    import tempfile
    from  tasks.crunch import convert_wav
    from  tasks.network import transcribe

    if content is None:
        current_job = get_current_job(redis_conn)
        content = get_first_dependent_result(network_queue, current_job)

    try:
        temp = tempfile.TemporaryFile()
        temp.write(content)
        temp.seek(0)

        convert_wav(temp)
        transcription = transcribe(temp)
        
        return transcription


    except Exception as exc:
        print(exc)
        temp.close()

    finally:
        temp.close()
