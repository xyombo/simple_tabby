
import argparse
import os
import json
import pyperclip
import sys

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.simple_tabby")
SSH_SERVER_CONFIGS = []


def connect(selected_config,args):
    host = selected_config['host']if 'host' in selected_config else 'localhost'
    user = selected_config['user']if 'user' in selected_config else 'root'
    port = selected_config['port']if 'port' in selected_config else 22
    passwd = selected_config['password'] if 'password' in selected_config else ''

    private_key = os.path.expanduser("~/.ssh/id_rsa")
    if 'privateKey' in selected_config:
        private_key = selected_config['privateKey']
    
    if (passwd):
        pyperclip.copy(passwd)
        print("trying to login server with ssh-key, if you has config password, the password has copied to clip, just pasted and enter!!")

    if (args.tunnet):
        ports = args.tunnet.split(":")
        command = f"ssh -L {ports[0]}:127.0.0.1:{ports[1]} -N -f {user}@{host}"
        print("run command :",command)
        i = os.system(command)

    os.system(f"ssh {user}@{host} -p {port} -i {private_key}")



   
def show_options():
    from simple_term_menu import TerminalMenu
    options = [SSH_SERVER_CONFIGS[i]['title'] for i in range(len(SSH_SERVER_CONFIGS))]
    ternimal_menu = TerminalMenu(options,show_search_hint=True,quit_keys=["q"])
    return ternimal_menu.show()

def save_file():
    with open(os.path.join(DEFAULT_CONFIG_PATH,'default.json'),'w') as f:
        f.write(json.dumps(SSH_SERVER_CONFIGS,indent=4,sort_keys=True))



def load_config():
    global SSH_SERVER_CONFIGS
    config_files = [config_file for config_file in os.listdir(DEFAULT_CONFIG_PATH) if config_file.endswith(".json")]
    for config_file in config_files:
        configs = json.loads(open(os.path.join(DEFAULT_CONFIG_PATH, config_file), encoding='utf-8').read())
        SSH_SERVER_CONFIGS = SSH_SERVER_CONFIGS+configs

def add(title,host,user='root',passwd=None,port="22"):
    SSH_SERVER_CONFIGS.append({
        'title':title,
        'host':host,
        'user':user,
        'password':passwd,
        'port':port
    })
    save_file()
   
def main():
    parser = argparse.ArgumentParser(description="Mini tool login remote ssh server ", add_help=True)

    parser.add_argument('-t', '--tunnet', type=str, required=False,nargs='?',
                    help="open tunnet with ssh localport:remoteport")

    args = parser.parse_args(['-t'])


    if sys.argv[1]=='login':

        load_config()
        selected_idx = show_options()
        selected_config = SSH_SERVER_CONFIGS[selected_idx]
        connect(selected_config)
    
    elif sys.argv[1] == 'add':
        from getpass import getpass
        title = input("Entry title:")
        host = input("Entry host:")
        user = input("Entry user name:")
        passwd = getpass(prompt="Enter password:"),
        port = input("Entry port,default is 22 :")
        add(
            title=title,
            host=host,
            user=user,
            passwd=passwd[0] if len(passwd)>1 else '',
            port=port
            )
    elif sys.argv[1] == ("del"):
       load_config()
       selected_idx = show_options()
       SSH_SERVER_CONFIGS.remove(selected_idx)
       save_file()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass