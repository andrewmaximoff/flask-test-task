from flask import Flask, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from core.config import Config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
moment = Moment()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('records.index'))

    from .views import auth, records
    csrf.exempt(auth.bp)
    csrf.exempt(records.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(records.bp)

    return app


if __name__ == '__main__':
    create_app().run()
