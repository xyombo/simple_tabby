import json
import os
import sys
import argparse
import pyperclip

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.simple_tabby")

SSH_SERVER_CONFIGS = []

config_files = [config_file for config_file in os.listdir(
    DEFAULT_CONFIG_PATH) if config_file.endswith(".json")]

for config_file in config_files:
    configs = json.loads(
        open(os.path.join(DEFAULT_CONFIG_PATH, config_file), encoding='utf-8').read())
    SSH_SERVER_CONFIGS = SSH_SERVER_CONFIGS+configs


def list_all_remote_servers():
    from prettytable import PrettyTable
    table = PrettyTable(['no', 'name', 'ip', 'apps', 'tags', 'description'])
    for i in range(0, len(SSH_SERVER_CONFIGS)):
        c = SSH_SERVER_CONFIGS[i]
        apps = ','.join(c['application'])
        tags = ','.join(c['tags'])
        describe = c['describe']
        table.add_row([i + 1, c['name'], c['host'], apps, tags, describe])
    print(table)


def select_one_to_login(no, tunne):
    c = SSH_SERVER_CONFIGS[no - 1]
    host = c['host']
    port = c['port']
    user = c['user']
    private_key = os.path.expanduser("~/.ssh/id_rsa")
    if 'privateKey' in c:
        private_key = c['privateKey']
    passwd = c['password']
    if (passwd):
        pyperclip.copy(passwd)

    print("trying to login server with ssh-key, if you has config password, the password has copied to clip, just pasted and enter!!")

    if (tunne):
        ports = tunne.split(":")
        os.system(f"ssh -L {ports[0]}:127.0.0.1:{ports[1]} {user}@{host}")
    else:
        os.system(f"ssh {user}@{host} -p {port} -i {private_key}")


def main():
    parser = argparse.ArgumentParser(description="Hello ", add_help=True)
    parser.add_argument('-ls', '--list', required=False,
                        action='store_true', help="list all configed servers")
    parser.add_argument('-c', '--connect', type=int,
                        required=False, help="connect to remote server by no")
    parser.add_argument('-t', '--tunnet', type=str, required=False,
                        help="open tunnet with ssh localport:remoteport")

    args = parser.parse_args()
    print(args)
    if (args.list):
        # list all remote server machine
        list_all_remote_servers()
    if (args.connect):
        select_one_to_login(args.connect, args.tunnet)


if __name__ == '__main__':
    main()
