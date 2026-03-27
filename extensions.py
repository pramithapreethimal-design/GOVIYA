from flask_mysqldb import MySQL
from flask_login import LoginManager

mysql = MySQL()
login_manager = LoginManager()

def init_app(app):
    """Initialize extensions with app config"""
    mysql.init_app(app)
    login_manager.init_app(app)