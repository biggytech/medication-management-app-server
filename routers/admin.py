from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route('/login')
def login():
    # TODO: implement
    return "Admin - Login"
