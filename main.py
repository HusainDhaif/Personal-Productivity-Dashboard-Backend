from fastapi import FastAPI
from controllers.users import router as UsersRouter

app = FastAPI()

app.include_router(UsersRouter, prefix="/api")

@app.get('/')
def home():
    return 'Hello World!'