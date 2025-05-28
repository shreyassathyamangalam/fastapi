# imports
from fastapi import FastAPI

# define app
app = FastAPI()

# define a simple route
@app.get("/")
def hello():
    return {"message": "Hello World"}

# define another route
@app.get("/about")
def about():
    return {"message": "This is a simple FastAPI application."}
