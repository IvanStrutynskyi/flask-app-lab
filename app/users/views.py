# app/users/views.py
from flask import Blueprint, request, redirect, url_for, render_template

# Створюємо Blueprint для маршруту users
users_bp = Blueprint('users', __name__)

@users_bp.route('/')
def main():
    return render_template("base.html")

@users_bp.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template("home.html", agent=agent)

@users_bp.route("/hi/<string:name>")  # маршрут /users/hi/<name>?age=45
def greetings(name):
    """Привітання користувача за іменем з параметром віку."""
    name = name.upper()
    age = request.args.get("age", None, int)  # отримуємо вік з параметрів URL
    return render_template("hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    """Перенаправлення на привітання адміністратора."""
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)  # _external для повного URL
    print(to_url)  # виводимо URL у консоль для відстеження
    return redirect(to_url)  # перенаправляємо на URL
