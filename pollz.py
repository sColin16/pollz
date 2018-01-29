from app import app, db
from app import routes
from app.models import Users, Polls, Responses


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users, 'Polls': Polls, 'Responses': Responses}
