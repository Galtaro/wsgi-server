from jinja2 import Template
from short_cuts import parse_body, parse_cookie
from datetime import datetime


COUNT = 1
db = {}
chat_message = []


def chat(request_method, http_cookie, body):
    body = parse_body(body)
    cookie = parse_cookie(http_cookie)
    user_id = int(cookie.get("user_id"))
    user_name = db.get(user_id)
    if user_name is None:
        return "307 Temporary Redirect", [("Location", "http://127.0.0.1:8000/register"),("Set-Cookie", "Location=chat")], b""
    with open("./templates/chat") as file:
        template = Template(file.read())
    if request_method == "POST" and (msg := body.get("msg")):
        chat_message.append(
            (user_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
        )
    return "200 OK", [], template.render(chat=chat_message).encode()


def view_register(request_method, http_cookie, body):
    if request_method == "GET":
        with open("./templates/register") as file:
            template = Template(file.read())
        return "200 OK", [], template.render().encode()
    body = parse_body(body)
    global COUNT
    db[COUNT] = body["name"]
    cookie = parse_cookie(http_cookie)
    if location := cookie.get("location"):
        response = "307 Temporary Redirect", [("Location", f"http://127.0.0.1:8000/{location}")], b""
    else:
        response = "200 OK", [("Set-Cookie", f"user_id={COUNT}")], b"register was success"
    COUNT += 1
    return response


def view_main(request_method, http_cookie, body):
    global COUNT
    with open("./templates/main") as file:
        template = Template(file.read())
    cookie = parse_cookie(http_cookie)
    user_id = int(cookie.get("user_id"))
    user_name = db.get(user_id)
    user_id = None
    if user_name is None:
        user_name = "undefined"
        user_id = COUNT
        COUNT += 1
    response = "200 OK", [], template.render(user_id=user_id, user_name=user_name).encode()
    return response


def view_cats(request_method, http_cookie, body):
    with open("./templates/cats") as file:
        template = Template(file.read())
    return "200 OK", [], template.render().encode()


def view_dogs(request_method, http_cookie, body):
    with open("./templates/dogs") as file:
        template = Template(file.read())
    return "200 OK", [], template.render().encode()

def view_static(request_method, http_cookie, body, image_name):
    with open(f"./static/{image_name}.jpg", "rb") as file:
        im_cont = file.read()
    return "200 OK", [], im_cont

def view_404(request_method, http_cookie, body):
    return "404 Not Found", [], b""
