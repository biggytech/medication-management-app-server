from flask import Flask
from routers.admin import admin
from routers.api import api

app = Flask(__name__)

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api, url_prefix='/api')

@app.route("/<uuid:name>")
def hello(name):
    return f"{name}"
