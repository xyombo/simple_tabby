import json
import os
import sys
import argparse
import pyperclip

configs = json.loads(
    open(os.path.expanduser("~/.simple_tabby/terminals_config.json"), encoding='utf-8').read())


def list_all_remote_servers():
    from prettytable import PrettyTable
    table = PrettyTable(['no', 'name', 'ip', 'apps', 'tags', 'description'])
    for i in range(0, len(configs)):
        c = configs[i]
        apps = ','.join(c['application'])
        tags = ','.join(c['tags'])
        describe = c['describe']
        table.add_row([i + 1, c['name'], c['host'], apps, tags, describe])
    print(table)


def select_one_to_login(no):
    c = configs[no - 1]
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

    os.system(f"ssh {user}@{host} -p {port} -i {private_key}")


def main():
    parser = argparse.ArgumentParser(description="Hello ", add_help=True)
    parser.add_argument('-ls', '--list', required=False,
                        action='store_true', help="list all configed servers")
    parser.add_argument('-c', '--connect', type=int,
                        required=False, help="connect to remote server by no")

    

    args = parser.parse_args()

    if (args.list):
        # list all remote server machine
        list_all_remote_servers()
    if (args.connect):
        select_one_to_login(args.connect)


if __name__ == '__main__':
    main()
