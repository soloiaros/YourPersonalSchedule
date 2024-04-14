from flask import Flask
from data.database import db_session
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import locale

from blueprints import user_bp


def create_app():
    locale.setlocale(
        category=locale.LC_ALL,
        locale="Russian"  # Note: do not use "de_DE" as it doesn't work
    )
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'MICHAEL_JORDAN_THE_BEST'

    db_session.global_init('data/database/app.sqlite')
    login_manager = LoginManager()
    login_manager.init_app(app)

    csrf = CSRFProtect()
    csrf.init_app(app)

    app.register_blueprint(user_bp.user_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        from data.database.users import User
        session = db_session.create_session()
        return session.query(User).get(user_id)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1', debug=True, threaded=True)