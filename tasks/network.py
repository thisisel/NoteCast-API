from tasks import (cpu_queue, get_current_job, get_first_dependent_result, job,
                network_queue, redis_conn)


@job(network_queue)
def get_content(url: str):
    from note_cast.utils import (ConnectTimeout, HTTPStatusError, Response,
                                    httpx_client_factory)
    
    client = httpx_client_factory()
    try:
        # TODO timeout = httpx.Timeout(read=240.0)
        with client:
            r: Response = client.get(url=url, timeout=None)
            return r.content

    except HTTPStatusError as exc:
        print(exc)

    except ConnectTimeout as exc:
        print(exc)

@job(network_queue)
def transcribe(temp):
    import speech_recognition as sr

    if temp is None:
        current_job = get_current_job(redis_conn)
        temp = get_first_dependent_result(cpu_queue, current_job)

    try:
        rec = sr.Recognizer()
        with sr.AudioFile(temp) as source:
            audio_data = rec.record(source)
            transcription = rec.recognize_google(audio_data)

            return transcription
    finally:
        temp.close()
