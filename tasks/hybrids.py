from tasks import (get_current_job, get_first_dependent_result, hybrid_queue,
                   job, network_queue, redis_conn)


@job(hybrid_queue)
def fetch_transcription_flow(content=None):
    import tempfile

    from tasks.crunch import convert_wav
    from tasks.network import transcribe

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

    finally:
        temp.close()
