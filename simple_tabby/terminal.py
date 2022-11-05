# /bin/bash/python3
import json
import os

# read remote server config file

configs = json.loads(
    open(os.path.expanduser("~/.simple_tabby/terminals_config.json"), encoding='utf-8').read())


def list_all_remote_servers():
    from prettytable import PrettyTable
    table = PrettyTable(['no', 'name', 'ip', 'apps', 'tags'])
    for i in range(0, len(configs)):
        c = configs[i]
        apps = ','.join(c['application'])
        tags = ','.join(c['tags'])
        table.add_row([i + 1, c['name'], c['host'], apps, tags])
    print(table)


def select_one_to_login(no):
    c = configs[no - 1]
    os.system(f"ssh root@{c['host']} -p {c['port']} -i {c['privateKey']}")


if __name__ == '__main__':
    # list all remote server machine
    list_all_remote_servers()
    configs_len = len(configs)
    print(f"please select one to login [1,{configs_len - 1}]: ", end="")
    no = input()
    select_one_to_login(int(no))
