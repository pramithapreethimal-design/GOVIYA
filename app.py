# 🔧 PyMySQL setup (MUST be first!)
import pymysql
pymysql.install_as_MySQLdb()

# 📦 Standard imports
import os
import sys
from flask import Flask, render_template, flash, redirect, url_for, request
from extensions import mysql, login_manager, init_app

# 🧩 Blueprint imports
from modules.auth import auth_bp
from modules.ai_scanner import scanner_bp
from modules.solutions import solutions_bp  
from modules.officers import officers_bp
from modules.community import community_bp

# 🚀 Create Flask app
app = Flask(__name__)

# 🔐 Secret Key
app.secret_key = os.environ.get('SECRET_KEY', 'goviya_final_viva_key_2026')

# 🗄️ Database Config (Defaults to LOCALHOST/XAMPP)
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '') 
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'goviya_db')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))

# ⏱️ Connection timeouts (helps with stability)
app.config['MYSQL_CONNECT_TIMEOUT'] = 30
app.config['MYSQL_READ_TIMEOUT'] = 60
app.config['MYSQL_WRITE_TIMEOUT'] = 60

# 🔒 SSL Config: ONLY for Aiven cloud (ignored for localhost)
if app.config['MYSQL_HOST'] and 'aivencloud.com' in app.config['MYSQL_HOST']:
    app.config['MYSQL_SSL'] = {'ssl_mode': 'REQUIRED'}

# 📁 Upload Folder
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔧 Initialize Extensions
init_app(app)
login_manager.login_view = 'auth.login' 

# 🧩 Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(scanner_bp)
app.register_blueprint(solutions_bp)  
app.register_blueprint(officers_bp)
app.register_blueprint(community_bp)

# ==================== ROUTES (ALL BEFORE if __name__) ====================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test')
def test():
    return "✅ Flask is working! Routes are loading!"

@app.route('/debug-db')
def debug_db():
    """Test database connection"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        return f"✅ Database connected! Result: {result}"
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {str(e)}"

@app.route('/routes')
def list_routes():
    """Debug: Show all registered routes"""
    output = []
    for rule in app.url_map.iter_rules():
        output.append(f"{rule.endpoint}: {rule.methods} {rule}")
    return "<br>".join(output)

# ==================== RUN APP (MUST BE LAST!) ====================

if __name__ == '__main__':
    if 'gunicorn' not in sys.modules:
        print("🚀 GOVIYA AI Platform Starting...")
        print(f"📡 Database Host: {app.config['MYSQL_HOST']}")
        print(f"📡 Database Port: {app.config['MYSQL_PORT']}")
        print(f"🗄️ Database Name: {app.config['MYSQL_DB']}")
        print("🧩 Modules: Auth, Scanner, Solutions, Community, Officers Loaded")
        print("🌐 Open in Browser: http://127.0.0.1:5000")
        print("🧪 Test Route: http://127.0.0.1:5000/test")
        print("🔍 Debug DB: http://127.0.0.1:5000/debug-db")
        print("🗺️  All Routes: http://127.0.0.1:5000/routes")
        
        app.run(host='0.0.0.0', port=5000, debug=False)