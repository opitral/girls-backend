from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from application.config import settings
from application.database import engine, Base
from application.initializer import Initializer
from application.routers import girl_router, service_router

app = FastAPI(title="Escort Service API", version="1.0.0")
app.mount("/photos", StaticFiles(directory="resources/photos"), name="photos")
app.include_router(girl_router)
app.include_router(service_router)

Base.metadata.create_all(bind=engine)

initializer = Initializer()
initializer.init_all()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.SERVER_HOST, port=settings.SERVER_PORT, reload=True)
