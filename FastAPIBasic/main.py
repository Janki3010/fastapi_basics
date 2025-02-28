from enum import Enum

import uvicorn
from fastapi import FastAPI, Query, Form, Request
import logging
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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


@app.get("/index", response_class=HTMLResponse)
def read_items(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, port=5300)