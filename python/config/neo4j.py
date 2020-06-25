import os
from dotenv import load_dotenv

load_dotenv()
user = os.environ.get("aura_user")
password = os.environ.get("aura_password")
uri = os.environ.get("aura_uri")

conf_neo4j = {
    "uri": uri,
    "password": password,
    "user": user
}
