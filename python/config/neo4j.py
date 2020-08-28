import os
from dotenv import load_dotenv

load_dotenv()

conf_neo4j = {
    "uri": os.environ.get("DO_HOST"),
    "password": os.environ.get("DO_PASSWORD"),
    "user": os.environ.get("DO_USER"),
}
