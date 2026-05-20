import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


TRANSLATIONS = {
    "es": {
        "app_name": "DOMINI",
        "login": "Iniciar sesion",
        "logout": "Cerrar sesion",
        "register": "Registrar usuario",
        "username": "Usuario",
        "password": "Contrasena",
        "dashboard": "Panel",
        "welcome": "Bienvenido a DOMINI",
        "dominus": "DOMINUS - reconocimiento de dominios",
        "sentinel": "SENTINEL - inteligencia de IPs",
        "invalid_credentials": "Usuario o contrasena invalidos",
        "user_exists": "El usuario ya existe",
        "user_created": "Usuario creado correctamente",
        "login_required": "Debes iniciar sesion para acceder",
    },
    "en": {
        "app_name": "DOMINI",
        "login": "Sign in",
        "logout": "Sign out",
        "register": "Register user",
        "username": "Username",
        "password": "Password",
        "dashboard": "Dashboard",
        "welcome": "Welcome to DOMINI",
        "dominus": "DOMINUS - domain reconnaissance",
        "sentinel": "SENTINEL - IP intelligence",
        "invalid_credentials": "Invalid username or password",
        "user_exists": "User already exists",
        "user_created": "User created successfully",
        "login_required": "Please sign in to access this page",
    },
    "ru": {
        "app_name": "DOMINI",
        "login": "Войти",
        "logout": "Выйти",
        "register": "Регистрация пользователя",
        "username": "Пользователь",
        "password": "Пароль",
        "dashboard": "Панель",
        "welcome": "Добро пожаловать в DOMINI",
        "dominus": "DOMINUS - разведка доменов",
        "sentinel": "SENTINEL - разведка IP",
        "invalid_credentials": "Неверное имя пользователя или пароль",
        "user_exists": "Пользователь уже существует",
        "user_created": "Пользователь создан",
        "login_required": "Войдите, чтобы открыть эту страницу",
    },
}


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'instance' / 'domini.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEFAULT_LANG = os.getenv("DEFAULT_LANG", "es")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "domini2024")
