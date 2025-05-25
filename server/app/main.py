from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware



origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


from .importer import importer
app.include_router(importer.router)
from .accounts import accounts
app.include_router(accounts.router)
from .users import users
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

