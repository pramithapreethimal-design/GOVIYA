from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, UserMixin
from extensions import mysql, login_manager

auth_bp = Blueprint('auth', __name__)

# --- User Class (Required for Flask-Login) ---
class User(UserMixin):
    def __init__(self, id, name, email, district):
        self.id = id
        self.name = name
        self.email = email
        self.district = district

# --- User Loader (Reloads user from session) ---
@login_manager.user_loader
def load_user(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, email, district FROM farmers WHERE id = %s", (user_id,))
        user_data = cur.fetchone()
        cur.close()
        if user_data:
            return User(id=user_data[0], name=user_data[1], email=user_data[2], district=user_data[3])
    except Exception as e:
        print(f"⚠️ load_user error: {e}")
    return None

# --- Routes ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        district = request.form.get('district')
        
        if not all([name, email, password, district]):
            flash("All fields are required", "warning")
            return redirect(url_for('auth.register'))
        
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')

        cur = None
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO farmers (name, email, password_hash, district) VALUES (%s, %s, %s, %s)", 
                        (name, email, hashed_pw, district))
            mysql.connection.commit()
            flash("Registration Successful! Please Login.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"❌ Register error: {e}")
            flash("Registration failed. Please try again.", "danger")
        finally:
            if cur:
                cur.close()
            
    return render_template("auth/register.html")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Email and password are required", "warning")
            return redirect(url_for('auth.login'))

        cur = None
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, name, email, password_hash, district FROM farmers WHERE email = %s", (email,))
            user_data = cur.fetchone()
            cur.close()

            if user_data and check_password_hash(user_data[3], password):
                user = User(id=user_data[0], name=user_data[1], email=user_data[2], district=user_data[4])
                login_user(user)
                flash(f"Welcome back, {user_data[1]}!", "success")
                return redirect(url_for('home'))
            elif user_data:
                flash("Incorrect Password", "danger")
            else:
                flash("Email not found", "danger")
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            flash("Login failed. Please try again.", "danger")
        finally:
            if cur:
                cur.close()

    return render_template("auth/login.html")

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))