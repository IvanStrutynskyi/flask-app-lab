# app/__init__.py
from flask import Flask
from .users.views import users_bp  # імпортуємо users_bp

app = Flask(__name__)

# Реєструємо Blueprint з префіксом /users
app.register_blueprint(users_bp, url_prefix="/users")
