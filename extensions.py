from flask_mysqldb import MySQL
from flask_login import LoginManager

# Initialize these here so other files can use them
mysql = MySQL()
login_manager = LoginManager()