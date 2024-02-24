from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.environ["MYSQL_HOST"]
MYSQL_PORT = os.environ["MYSQL_PORT"]
MYSQL_USER = os.environ["MYSQL_USER"]
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_DATABASE = os.environ["MYSQL_DATABASE"]
MYSQL_ENABLED = os.environ["MYSQL_ENABLED"] == "1"

# Maybe these should be db?
DISCORD_URL = os.environ["DISCORD_URL"]
DOWNLOAD_PC = os.environ["DOWNLOAD_PC"]
DOWNLOAD_ANDROID = os.environ["DOWNLOAD_ANDROID"]
