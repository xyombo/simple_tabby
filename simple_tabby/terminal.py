import json
import os
import sys
import time

import pyperclip

start = time.time()
configs = json.loads(
    open(os.path.expanduser("~/.simple_tabby/terminals_config.json"), encoding='utf-8').read())
end = time.time()


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
        private_key = c
    passwd = c['password']
    pyperclip.copy(passwd)
    print("trying to login server with ssh-key, if you has config password, the password has copied to clip, just pasted and enter!!")
    os.system(f"ssh {user}@{host} -p {port} -i {private_key}")


if __name__ == '__main__':
    argv_len = len(sys.argv)
    no = 0
    if argv_len == 2:
        no = sys.argv[1]
    else:
        # list all remote server machine
        list_all_remote_servers()
        configs_len = len(configs)
        print(f"please select one to connect [1,{configs_len}] (input 0 for cancel) :", end="")
    if 0 >= int(no):
        sys.exit()
    select_one_to_login(int(no))
