import os
from dotenv import load_dotenv

load_dotenv()

SIGNING_KEY = os.environ.get("SQL_DATABASE")

print(SIGNING_KEY)


