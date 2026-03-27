from flask_mysqldb import MySQL
from flask_login import LoginManager

mysql = MySQL()
login_manager = LoginManager()

def init_app(app):
    """Initialize extensions with app config"""
    mysql.init_app(app)
    login_manager.init_app(app)
    
    # 🔒 SSL Config for Aiven Cloud MySQL
    if app.config.get('MYSQL_HOST') and 'aivencloud.com' in app.config.get('MYSQL_HOST', ''):
        app.config['MYSQL_SSL'] = {'ssl_mode': 'REQUIRED'}
        # Optional: If Aiven provides a CA certificate, add:
        # app.config['MYSQL_SSL_CA'] = '/path/to/ca.pem'