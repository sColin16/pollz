import os
os.environ["DATABASE_URL"] = "sqlite:///dev.db"
print(os.getenv("DATABASE_URL"))

from app import db  # pylint:disable=E0611,C0413,W0403
db.create_all()
