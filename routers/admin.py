from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route('/login')
def login():
    return "Admin - Login"
