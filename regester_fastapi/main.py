from fastapi import FastAPI, Form, HTTPException
import pymysql
import uvicorn
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi import BackgroundTasks

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


DB_HOST = "localhost"
DB_USER = "username"
DB_PASSWORD = "password"
DB_NAME = "db_name"

def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
    )
    return connection

@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("regester.html", {"request": request})

@app.post("/register_post")
async def post_register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
):

    print(f"Username: {username}, Email: {email}, Password: {password}, Phone: {phone}")
    message = f"User {username} registered successfully"
    write_notification(email, message)

    # You can return a message or redirect somewhere else
    return {"message": f"User {username} registered successfully with email {email}"}

def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


if __name__ == "__main__":
    uvicorn.run(app, port=5400)