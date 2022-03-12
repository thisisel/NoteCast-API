from datetime import timedelta

from rq.exceptions import NoSuchJobError
from rq import Queue, get_current_job
from rq.job import Job
from rq.decorators import job
from rq.registry import ScheduledJobRegistry

# redis_conn = redis.from_url("redis://localhost:6379")
from worker import redis_conn

network_queue = Queue(name="network", connection=redis_conn)
cpu_queue = Queue(name="cpu", connection=redis_conn)

network_registry = ScheduledJobRegistry(queue=network_queue)

def get_first_dependent_result(origin_queue, current_job):
    first_job_id = current_job.dependencies[0].id
    first_job_result = origin_queue.fetch_job(first_job_id).result

    return first_job_result

class CrunchTasks:
    @classmethod
    @job(cpu_queue)
    def convert_wav(cls, temp=None):
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


class DBtasks:
    @classmethod
    @job(cpu_queue)
    def update_transcription(cls, q_id, transcript):
        from note_cast.db.crud.quote import QuoteQuery

        if transcript is None:
            current_job = get_current_job(redis_conn)
            transcript = get_first_dependent_result(network_queue, current_job)

        QuoteQuery.update_transcript(q_id=q_id, transcript=transcript)


class FileTasks:
    @classmethod
    def close_temp_file(cls, job, connection, type, value, traceback):
        temp = job.kwargs.get("temp")
        temp.close()

    @classmethod
    @job(cpu_queue)
    def create_temp_file(cls, content=None):
        import tempfile

        if content is None:
            current_job = get_current_job(redis_conn)
            content = get_first_dependent_result(network_queue, current_job)

        try:
            temp = tempfile.TemporaryFile()
            temp.write(content)
            temp.seek(0)

            return temp

        except Exception as exc:
            print(exc)
            temp.close()


class NetworkTasks:
    @classmethod
    @job(network_queue)
    def get_content(cls, url: str):
        from note_cast.utils import (ConnectTimeout, HTTPStatusError, Response,
                                     httpx_client)

        try:
            # TODO timeout = httpx.Timeout(read=240.0)
            with httpx_client as client:
                r: Response = client.get(url=url, timeout=None)
                return r.content

        except HTTPStatusError as exc:
            print(exc)

        except ConnectTimeout as exc:
            print(exc)

    @classmethod
    @job(network_queue)
    def transcribe(cls, temp):
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



def pull_transcript(p_id: str, e_id: str, q_id: str, transcript: str):
    from note_cast.db.crud.quote import QuoteQuery
    from note_cast.services.cloudinary_api import asset_folder_path
    from note_cast.services.cloudinary_api.resource import CloudinaryResource

    try:
        asset_path = asset_folder_path(p_id=p_id, e_id=e_id)
        transcript_public_id = f"{asset_path}{q_id}.transcript"

        # resource_info_response = CloudinaryResource.get_resource_info(public_id=raw_public_id, resource_type="raw")
        # resource_data = CloudinaryResource.download_resource(resource_info_response["url"])
        # resource_data_jsn = resource_data.json()
        # transcript = resource_data_jsn[0]["transcript"]

        transcript = CloudinaryResource.fetch_transcript(
            public_id=transcript_public_id, resource_type="raw"
        )

        # TODO make it either on_successful call back or dependency
        QuoteQuery.update_transcript(q_id=q_id, transcript=transcript)

    except Exception as x:
        print(x)


class JobSchedueler:
    @classmethod
    def schedule_transcript_job(cls, seconds, *args, **kwargs):
        job = network_queue.enqueue_in(
            timedelta(seconds=seconds), pull_transcript, *args, **kwargs
        )
        return job

    @classmethod
    def cancel_scheduled_job(cls, job_id):
        try:
            job = Job.fetch(job_id, connection=redis_conn)
            network_registry.remove(job=job, delete_job=True)
        except NoSuchJobError as nse:
            # TODO log with worker logger
            print(nse)




class Pipelines:
    @classmethod
    def begin_transcribe_fallback(cls, audio_url: str, q_id: str):


        
        # 1. download resource(network)!!LONG RUNNING
        download_job = NetworkTasks.get_content.delay(audio_url)
        
        # 2. create temp file (cpu)
        temp_file_job = FileTasks.create_temp_file.delay(depends_on=download_job)
        
        # 3. convert mp3 to wav(cpu)!!A LONG RUNNING TASK DEPENDS ON IT-> KEEP RESULTS LONGER
        convert_job = CrunchTasks.convert_wav.delay(depends_on=temp_file_job)
        
        # 4. transcribe (network)!!LONG RUNNING
        transcription_job = NetworkTasks.transcribe.delay(depends_on=convert_job)
        
        # 5.  update transcription
        _ = DBtasks.update_transcription.delay(
            q_id=q_id,
            depends_on=transcription_job,
        )