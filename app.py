import os
from flask import Flask, render_template
from extensions import mysql, login_manager


from modules.auth import auth_bp
from modules.ai_scanner import scanner_bp
from modules.solutions import solutions_bp  
from modules.officers import officers_bp
from modules.community import community_bp

app = Flask(__name__)


app.secret_key = os.environ.get('SECRET_KEY', 'goviya_final_viva_key_2026')



app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '') 
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'goviya_db')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))


UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


os.makedirs(UPLOAD_FOLDER, exist_ok=True)


mysql.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login' 


app.register_blueprint(auth_bp)
app.register_blueprint(scanner_bp)
app.register_blueprint(solutions_bp)
app.register_blueprint(officers_bp)
app.register_blueprint(community_bp)


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
   
    import sys
    if 'gunicorn' not in sys.modules:
        print(" GOVIYA AI Platform Starting...")
        print(" Database: Connected to XAMPP")
        print(" Modules: Auth, Scanner, Solutions, Community, Officers Loaded")
        print(" Open in Browser: http://127.0.0.1:5000")
        
        app.run(host='0.0.0.0', port=5000, debug=False)
        
        app.config['MYSQL_SSL'] = {'ssl_mode': 'REQUIRED'}