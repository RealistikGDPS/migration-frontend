from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.environ["MYSQL_HOST"]
MYSQL_PORT = os.environ["MYSQL_PORT"]
MYSQL_USER = os.environ["MYSQL_USER"]
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_DATABASE = os.environ["MYSQL_DATABASE"]
