from fastapi import status
import speech_recognition as sr
from note_cast.api.errors import CustomHTTPException, SPEECH_REC_500
from note_cast.log.custom_logging import loguru_app_logger


class GoogleTranscription:

    recognizer = sr.Recognizer()

    @classmethod
    def get_transcription(cls, filename):
        try:
            with sr.AudioFile(filename) as source:
                audio_data = cls.recognizer.record(source)
                transcript = cls.recognizer.recognize_google(audio_data)

                return transcript

        except Exception as exc:
            loguru_app_logger.exception(exc)
            raise CustomHTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                category=SPEECH_REC_500,
                detail="ERROR in getting transcription from google speech recognition service",
            )
