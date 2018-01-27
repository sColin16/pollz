"""This file imports necessary objects and classes from the app module so
that they can be easily used in all testing files"""

import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../app')))


from app import app, db, Users, Polls, Responses, sha256_crypt  # pylint:disable=E0611,C0413,W0611
