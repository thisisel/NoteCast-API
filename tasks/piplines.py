
import sys

sys.path.append("..")




def begin_transcribe_fallback(audio_url: str, q_id: str):

    from tasks.network import get_content, transcribe
    from tasks.hybrids import fetch_transcription_flow
    from tasks.crunch import convert_wav
    from tasks.database import update_transcription
    
    # 1. download resource(network)!!LONG RUNNING
    download_job = get_content.delay(audio_url)
    
    # 2. create temp file (cpu)
    transcription_flow_job = fetch_transcription_flow.delay(depends_on=download_job)
    
    # # 3. convert mp3 to wav(cpu)!!A LONG RUNNING TASK DEPENDS ON IT-> KEEP RESULTS LONGER
    # convert_job = convert_wav.delay(depends_on=temp_file_job)
    
    # 4. transcribe (network)!!LONG RUNNING
    # transcription_job = transcribe.delay(depends_on=transcription_flow_job)
    
    # 5.  update transcription
    _ = update_transcription.delay(
        q_id=q_id,
        depends_on=transcription_flow_job,
        )
