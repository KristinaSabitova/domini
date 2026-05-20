from pathlib import Path

from OpenSSL import crypto
from flask import Flask, g, request

from config import Config, TRANSLATIONS
from domini.extensions import bcrypt, db, login_manager


def create_self_signed_cert(cert_dir: Path) -> tuple[str, str]:
    cert_dir.mkdir(parents=True, exist_ok=True)
    cert_file = cert_dir / "domini.crt"
    key_file = cert_dir / "domini.key"

    if cert_file.exists() and key_file.exists():
        return str(cert_file), str(key_file)

    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)

    cert = crypto.X509()
    subject = cert.get_subject()
    subject.C = "ES"
    subject.ST = "Madrid"
    subject.L = "Madrid"
    subject.O = "DOMINI"
    subject.OU = "OSINT"
    subject.CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
    cert.set_issuer(subject)
    cert.set_pubkey(key)
    cert.sign(key, "sha256")

    cert_file.write_bytes(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    key_file.write_bytes(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    return str(cert_file), str(key_file)


def create_admin_user() -> None:
    from domini.models.user import User

    admin = User.query.filter_by(username=Config.ADMIN_USERNAME).first()
    if admin:
        return

    admin = User(username=Config.ADMIN_USERNAME)
    admin.set_password(Config.ADMIN_PASSWORD)
    db.session.add(admin)
    db.session.commit()


def create_app() -> Flask:
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder="domini/static",
        template_folder="domini/templates",
    )
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = TRANSLATIONS["es"]["login_required"]

    from domini.auth.routes import auth_bp
    from domini.dashboard.routes import dashboard_bp
    from domini.models.user import User

    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:
        return db.session.get(User, int(user_id))

    @app.before_request
    def set_locale() -> None:
        lang = request.args.get("lang") or request.cookies.get("lang") or Config.DEFAULT_LANG
        g.lang = lang if lang in TRANSLATIONS else Config.DEFAULT_LANG
        g.t = TRANSLATIONS[g.lang]

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    with app.app_context():
        db.create_all()
        create_admin_user()

    return app


app = create_app()


if __name__ == "__main__":
    cert_path, key_path = create_self_signed_cert(Path("certs"))
    app.run(host="localhost", port=8443, ssl_context=(cert_path, key_path))
