"""This file creates all the tables in the database.
Run only only after DATABASE_URL has been set with
export DATABASE_URL=sqlite:///dev.db"""

from app import db  # pylint:disable=E0611,C0413,W0403
db.create_all()
