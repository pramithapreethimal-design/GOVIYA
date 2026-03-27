import os
import sys
from flask import Flask, render_template, flash, redirect, url_for, request
from extensions import mysql, login_manager

from modules.auth import auth_bp
from modules.ai_scanner import scanner_bp
from modules.solutions import solutions_bp  
from modules.officers import officers_bp
from modules.community import community_bp

app = Flask(__name__)

# 🔐 Secret Key (from env or fallback)
app.secret_key = os.environ.get('SECRET_KEY', 'goviya_final_viva_key_2026')

# 🗄️ Database Config (from env or fallback to localhost)
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '') 
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'goviya_db')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))

# 🔒 SSL Config for Aiven (ONLY if using cloud DB)
if os.environ.get('MYSQL_HOST') and 'aivencloud.com' in os.environ.get('MYSQL_HOST', ''):
    app.config['MYSQL_SSL'] = {'ssl_mode': 'REQUIRED'}
    # Note: For full SSL with CA cert, you'd need to download Aiven's ca.pem
    # For demo, ssl_mode=REQUIRED often works without the CA file

# 📁 Upload Folder
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔧 Initialize Extensions
mysql.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login' 

# 🧩 Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(scanner_bp)
app.register_blueprint(solutions_bp)  
app.register_blueprint(officers_bp)
app.register_blueprint(community_bp)

# 🏠 Home Route
@app.route('/')
def home():
    return render_template('index.html')

# 🧪 Demo Mode Helper (Optional - for LinkedIn demo)
@app.before_request
def demo_mode_notice():
    """Show a flash message if demo mode is enabled"""
    if os.environ.get('DEMO_MODE') == 'True':
        flash("🔹 Demo Mode: UI is functional. Database operations limited for public access.", "info")

# 🚀 Run App
if __name__ == '__main__':
    # Only run directly if not using gunicorn (for local/ngrok testing)
    if 'gunicorn' not in sys.modules:
        print("🚀 GOVIYA AI Platform Starting...")
        print(f"📡 Database Host: {app.config['MYSQL_HOST']}")
        print("🧩 Modules: Auth, Scanner, Solutions, Community, Officers Loaded")
        print("🌐 Open in Browser: http://127.0.0.1:5000")
        print("💡 Tip: Set DEMO_MODE=True for LinkedIn demo (optional)")
        
        app.run(host='0.0.0.0', port=5000, debug=False)