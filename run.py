import uvicorn

from note_cast.app import settings, app

if __name__ == "__main__":
    uvicorn.run("run:app", host=settings.HOST, port=settings.PORT, reload=True)
