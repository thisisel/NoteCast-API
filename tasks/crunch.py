from tasks import job, cpu_queue, get_current_job, get_first_dependent_result, redis_conn


@job(cpu_queue)
def convert_wav(temp=None):
    from pydub import AudioSegment

    if temp is None:
        current_job = get_current_job(redis_conn)
        temp = get_first_dependent_result(cpu_queue, current_job)

    try:
        converter = AudioSegment.from_file_using_temporary_files(temp)
        converter.export(temp, format="wav")
        temp.seek(0)

        return temp

    except Exception as exc:
        print(exc)
        temp.close()
