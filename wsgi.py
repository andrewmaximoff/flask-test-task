from core import create_app, db
from core.models import User, Record

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Record': Record}


if __name__ == "__main__":
    app.run()
