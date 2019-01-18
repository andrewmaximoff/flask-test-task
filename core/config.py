import os

# basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '__CHANGE-ME__'
    POSTGRES = {
        'user': os.getenv('APPLICATION_POSTGRES_USER', 'postgres'),
        'pw': os.getenv('APPLICATION_POSTGRES_PW', ''),
        'host': os.getenv('APPLICATION_POSTGRES_HOST', 'localhost'),
        'port': os.getenv('APPLICATION_POSTGRES_PORT', 5432),
        'db': os.getenv('APPLICATION_POSTGRES_DB', 'postgres'),
    }
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES["user"]}:' \
        f'{POSTGRES["pw"]}@{POSTGRES["host"]}:{POSTGRES["port"]}/{POSTGRES["db"]}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 3
