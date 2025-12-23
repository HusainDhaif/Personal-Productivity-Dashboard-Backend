from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI()


@app.get("/")
def read_root():
    """
    Simple root route to test that the server is running.
    """
    return {"message": "Personal Productivity Dashboard API is running"}