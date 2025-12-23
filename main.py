from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.users import router as UsersRouter

app = FastAPI()

# Allowed origins for the React frontend.
# Adjust or move to environment config as needed.
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UsersRouter, prefix="/api")


@app.get("/")
def home():
    return "Hello World!"