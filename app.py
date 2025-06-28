from flask import Flask
from admin import init_admin_router

app = Flask(__name__)

init_admin_router('admin', app)

@app.route("/<name>")
def hello(name):
    return f"{name}"
