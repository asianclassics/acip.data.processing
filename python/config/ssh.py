import os
from dotenv import load_dotenv
load_dotenv()

conf_ssh = {
    "config_path": os.environ['SSH_CONFIG_PATH'],
    "host": os.environ['SSH_HOST'],
    "user": os.environ['SSH_USER'],
    "remote_path": "/home/bdrc_sync/newest_xml.xml",
    "local_file_name": "newest_xml.xml"
}
