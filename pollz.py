"""File that FLASK_APP should be set to. This allows the usage
of make run (for running the dev server), and flask shell
(for debugging the app)"""

from app import app, db, routes  # pylint:disable=unused-import
from app.models import Users, Polls, Responses


@app.shell_context_processor
def make_shell_context():
    """Flask testing shell that can be running by calling 'flask shell',
    given that FLASK_APP has been set to pollz.py"""

    return {'db': db, 'Users': Users, 'Polls': Polls, 'Responses': Responses}
