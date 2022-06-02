
import sys

sys.path.append("..")




def trigger_transcription_fallback(url: str, q_id: str):
    """
       Download audio clip from network 
       and request transcription from google.
       All tasks performed in the background.
       
        cpu, network and hybrid queue.

        1. download resource(network)!!LONG RUNNING
        2. create temp file (cpu)
        3. convert mp3 to wav(cpu)!!A LONG RUNNING TASK DEPENDS ON IT-> KEEP RESULTS LONGER
        4. transcribe (network)!!LONG RUNNING
        5.  update transcription
    
    Args:
        audio_url (str): http url pattern_
        q_id (str): id of a premature quote waiting for transcription
    """

    from tasks.network import get_content
    from tasks.hybrids import fetch_transcription_flow
    from tasks.database import update_transcription
    
    download_job = get_content.delay(url)
    transcription_flow_job = fetch_transcription_flow.delay(depends_on=download_job)
    _ = update_transcription.delay(
        q_id=q_id,
        depends_on=transcription_flow_job,
        )
