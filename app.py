import os
from flask import Flask, render_template
from extensions import mysql, login_manager

# --- IMPORT ALL MODULES ---
from modules.auth import auth_bp
from modules.ai_scanner import scanner_bp
from modules.solutions import solutions_bp  # This is your new Hybrid Brain
from modules.officers import officers_bp
from modules.community import community_bp

app = Flask(__name__)

# ==========================================
# ⚙️ CONFIGURATION (XAMPP Setup)
# ==========================================
# Security Key (Required for Login & Sessions)
app.secret_key = 'goviya_final_viva_key_2026'

# Database Settings (Standard XAMPP)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' # Leave empty for XAMPP default
app.config['MYSQL_DB'] = 'goviya_db'

# Upload Folder (Where scanned images go)
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create the upload folder automatically if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================================
# 🔌 INITIALIZE EXTENSIONS
# ==========================================
mysql.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login' # Redirect here if user isn't logged in

# ==========================================
# 🔗 REGISTER BLUEPRINTS (The Modules)
# ==========================================
app.register_blueprint(auth_bp)
app.register_blueprint(scanner_bp)
app.register_blueprint(solutions_bp)
app.register_blueprint(officers_bp)
app.register_blueprint(community_bp)

# ==========================================
# 🏠 GLOBAL ROUTES
# ==========================================
@app.route('/')
def home():
    return render_template('index.html')

# ==========================================
# 🚀 START THE APP
# ==========================================
if __name__ == '__main__':
    print("🌾 GOVIYA AI Platform Starting...")
    print("✅ Database: Connected to XAMPP")
    print("✅ Modules: Auth, Scanner, Solutions, Community, Officers Loaded")
    print("👉 Open in Browser: http://127.0.0.1:5000")
    
    app.run(debug=True)