from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super-secret-key-change-this-in-production"

# Database Configuration (SQLite database file: login_page.db)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///login_page.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# User Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# HTML Template for Login Page, Registration, and Dashboard
LOGIN_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page - {{ title }}</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: #1e293b; padding: 30px; border-radius: 12px; border: 1px solid #334155; width: 100%; max-width: 380px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
        h2 { margin-top: 0; color: #f1f5f9; text-align: center; }
        .form-group { margin-bottom: 16px; }
        label { display: block; font-size: 13px; color: #94a3b8; margin-bottom: 6px; }
        input { width: 100%; padding: 10px 12px; background: #0f172a; border: 1px solid #334155; border-radius: 6px; color: #fff; font-size: 14px; outline: none; }
        input:focus { border-color: #6366f1; }
        button { width: 100%; padding: 10px; background: #6366f1; border: none; border-radius: 6px; color: #fff; font-weight: 600; font-size: 14px; cursor: pointer; margin-top: 10px; }
        button:hover { background: #4f46e5; }
        .alert { padding: 10px; border-radius: 6px; font-size: 13px; margin-bottom: 16px; background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; color: #fca5a5; }
        .success { background: rgba(34, 197, 94, 0.2); border-color: #22c55e; color: #86efac; }
        .link { text-align: center; font-size: 13px; margin-top: 16px; color: #94a3b8; }
        .link a { color: #818cf8; text-decoration: none; }
        .link a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="card">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert {% if category == 'success' %}success{% endif %}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% if view == 'login' %}
            <h2>Login</h2>
            <form method="POST" action="{{ url_for('login_page') }}">
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" name="username" required autocomplete="off">
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit">Sign In</button>
            </form>
            <div class="link">
                Don't have an account? <a href="{{ url_for('register') }}">Register</a>
            </div>

        {% elif view == 'register' %}
            <h2>Create Account</h2>
            <form method="POST" action="{{ url_for('register') }}">
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" name="username" required autocomplete="off">
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit">Sign Up</button>
            </form>
            <div class="link">
                Already registered? <a href="{{ url_for('login_page') }}">Login</a>
            </div>

        {% elif view == 'dashboard' %}
            <h2>Welcome, {{ username }}!</h2>
            <p style="text-align: center; color: #94a3b8; font-size: 14px;">You have successfully logged in.</p>
            <a href="{{ url_for('logout') }}"><button type="button" style="background: #ef4444;">Logout</button></a>
        {% endif %}
    </div>
</body>
</html>
"""


# --- ROUTES ---

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login_page"))


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if "user" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["user"] = user.username
            flash("Successfully logged in!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "error")

    return render_template_string(LOGIN_PAGE_TEMPLATE, view="login", title="Sign In")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please pick another.", "error")
        elif len(password) < 4:
            flash("Password must be at least 4 characters long.", "error")
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created! Please log in.", "success")
            return redirect(url_for("login_page"))

    return render_template_string(LOGIN_PAGE_TEMPLATE, view="register", title="Register")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for("login_page"))
    return render_template_string(LOGIN_PAGE_TEMPLATE, view="dashboard", title="Dashboard", username=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("login_page"))


# Initialize Database and Start Server
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)