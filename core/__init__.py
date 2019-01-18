from flask import Flask, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cache import Cache
from flask_session import Session

from core.config import Config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
moment = Moment()
cache = Cache(config=Config.CACHE)
session = Session()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    cache.init_app(app)
    session.init_app(app)

    @app.route('/')
    @cache.cached(timeout=50)
    def index():
        return redirect(url_for('records.index'))

    from .views import auth, records
    csrf.exempt(auth.bp)
    csrf.exempt(records.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(records.bp)

    from .views.error import page_not_found, internal_server_error, forbidden
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(403, forbidden)

    return app


if __name__ == '__main__':
    create_app().run()
