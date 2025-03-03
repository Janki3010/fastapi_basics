from enum import Enum

import uvicorn
from fastapi import FastAPI, Query, Form, Request
import logging
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()


# Set the path for your templates folder
templates = Jinja2Templates(directory="templates")

@app.get("/read_item", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello, FastAPI!"})


# Mount static folder at '/static'
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set the path for your templates folder
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # You can pass variables to the template here
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello, FastAPI!"})

logging.basicConfig(level=logging.DEBUG)

class Choice_name(str, Enum):
    first = "Tae"
    second = "JK"
    third = "Jin"

class Student(BaseModel):
    RollNo: int
    Name: str
    Marks: float

@app.get('/')
def home():
    return {"message": "Hello World!"}

@app.get('/item/{Item}')
def path_fun(Item: int):
    return {"Item": Item}

@app.get('/query')
def query_func(id: str= Query(default=None, min_length=2, max_length=10), name: str= Query(default=None, min_length=2, max_length=10)):
    return {"RollNo": int(id), "Name": name}

@app.get('/models/{model_name}')
def get_model(model_name: Choice_name):
    return {"Name": model_name}

@app.get('/select_name/{name}')
def get_selected_name(name: Choice_name):
    if name.value == "Tae":
        return {"name": name, "message": f"Calling {name}"}

    if name.value == "JK":
        return {"name": name, "message": f"Calling {name}"}

    else:
        return {"name": name, "message": f"Calling {name}"}

@app.post('/students/')
def create_student(student_data: Student):
    return student_data

@app.post("/form/data")
def form_data(username: str = Form(), password: str= Form()):
    return ({"User Name": username, "Password": password})

from fastapi import BackgroundTasks, FastAPI

def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


if __name__ == "__main__":
    uvicorn.run(app, port=5300)