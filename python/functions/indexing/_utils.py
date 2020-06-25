from generate_acip_schema import BXml
from paramiko import SSHClient, SSHConfig
from scp import SCPClient
from indexing.config.print_logger import Logger
from indexing.config.logging import conf_log
import os
import sys
import logging


# -------------------------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------------------
def configure_logger():
    # configure the logger
    sys.stdout = Logger()
    # levels: debug, info, warning, error, critical
    # example --> logging.warning('This will get logged to a file')
    logging.basicConfig(
        # level=logging.DEBUG,
        filename=conf_log["filename"],
        filemode=conf_log["mode"],
        format=conf_log["formatter"]
    )


# -------------------------------------------------------------------------------------------------
# add try / catch to this!
# -------------------------------------------------------------------------------------------------

def get_xml(config):
    current_dir = os.getcwd()
    local_path = os.path.join(current_dir, 'data', config['local_file_name'])
    print(local_path)
    if not os.path.exists(local_path):
        ssh = SSHClient()
        ssh.load_system_host_keys()

        ssh_config = SSHConfig.from_path(config['config_path'])
        e = ssh_config.lookup(config['host'])
        ssh.connect(e['hostname'], username=e['user'])

        # SCPClient takes a Paramiko transport as an argument
        scp = SCPClient(ssh.get_transport())
        scp.get(remote_path=config['remote_path'], local_path=local_path)
        scp.close()

    return local_path


# -------------------------------------------------------------------------------------------------
# take an array, sort and unique-fy
# -------------------------------------------------------------------------------------------------
def make_unique(listing):
    full_listing = sorted(listing)
    unique_listing = []
    for n, item in enumerate(full_listing):
        if item not in full_listing[n + 1:]:
            unique_listing.append(item)

    return unique_listing


# -------------------------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------------------
def get_listing_by_type(get_type, elastic_instance, instance=None, file=None, gs_key=None, es_index_version="v4",
                        filter_by_collection=None, filter_by_distance=None):

    listing = []

    if instance is None:
        instance = elastic_instance
    if get_type == 'xml':
        listing = BXml(file).get_listing()
    elif get_type == 'gs':
        listing = instance.get_listing(ws=gs_key)
    elif get_type == 'resources':
        listing = instance.get_listing(es_index_version, node="_resources", filter_by_collection=filter_by_collection,
                                       filter_by_distance=filter_by_distance)

    print(f"New listings: {len(listing)}, {listing}")
    # get rid of I's (we don't actually use this type)
    listing = [x for x in listing if x[0] != 'I']
    print(f"Excluding the I (items) BDRC type >> {len(listing)}")

    existing_listing = elastic_instance.get_listing(es_index_version)
    print(f"Current ElasticSearch index of {len(existing_listing)} items, {existing_listing}")

    # find new listings not already indexed in ES
    new_listing = [x for x in listing if x not in existing_listing]

    if len(new_listing) > 0:
        print(f"To be indexed: {len(new_listing)} items, {new_listing}")

    return [new_listing, existing_listing]
