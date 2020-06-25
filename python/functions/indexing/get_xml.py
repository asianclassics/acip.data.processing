import os
from paramiko import SSHClient, SSHConfig
from scp import SCPClient


def get_xml(config):
    current_dir = os.getcwd()
    local_path = os.path.join(current_dir, '../data/xml', config['local_file_name'])
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
