from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.database.database import Base, engine

from app.routers.auth import router as auth_router


app = FastAPI(title="FastAPI Auth API", version="1.0.0")


Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)


@app.get("/")
def home():

    return {"message": "API running"}
