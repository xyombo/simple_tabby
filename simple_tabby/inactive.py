import os
import json

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.simple_tabby")
SSH_SERVER_CONFIGS = []

config_files = [config_file for config_file in os.listdir(DEFAULT_CONFIG_PATH) if config_file.endswith(".json")]
for config_file in config_files:
    configs = json.loads(open(os.path.join(DEFAULT_CONFIG_PATH, config_file), encoding='utf-8').read())
    SSH_SERVER_CONFIGS = SSH_SERVER_CONFIGS+configs



def login(sconfig):
    from ssh_client import SSH    
    host = sconfig['host']if 'host' in sconfig else 'localhost'
    user = sconfig['user']if 'user' in sconfig else 'root'
    port = sconfig['port']if 'port' in sconfig else 22
    passwd = sconfig['password'] if 'password' in sconfig else ''

    private_key = os.path.expanduser("~/.ssh/id_rsa")
    if 'privateKey' in sconfig:
        private_key = sconfig['privateKey']

    ssh = SSH(host,user,port,passwd,private_key)
    ssh.open_shell()
    pass

def tunnet(sconfig):
    from ssh_client import SSH    
    host = sconfig['host']if 'host' in sconfig else 'localhost'
    user = sconfig['user']if 'user' in sconfig else 'root'
    port = sconfig['port']if 'port' in sconfig else 22
    passwd = sconfig['password'] if 'password' in sconfig else ''

    private_key = os.path.expanduser("~/.ssh/id_rsa")
    if 'privateKey' in sconfig:
        private_key = sconfig['privateKey']
    
    local_port = input("please entery local port number :")
    remote_port = input("please entery remote port number :")
    ssh = SSH(host,user,port,passwd,private_key)
    ssh.open_tunnet(local_port,remote_port)


def pc(args):
    if args is not None:
        for config in SSH_SERVER_CONFIGS:
            if config['title']==args :
                return f"host:{config['host']} \nport:{config['port']}\nuser:{config['user']}\n"
    return None
   

def show_options():
    from simple_term_menu import TerminalMenu
    options = [SSH_SERVER_CONFIGS[i]['title'] for i in range(len(SSH_SERVER_CONFIGS))]
    ternimal_menu = TerminalMenu(options,show_search_hint=True,quit_keys=["q"],preview_command=pc, preview_size=0.75)
    return ternimal_menu.show()
    
def show_actions():
    from simple_term_menu import TerminalMenu
    options = ['login','open tunnet']
    ternimal_menu = TerminalMenu(options,show_search_hint=True,quit_keys=["q"],preview_command=pc, preview_size=0.75)
    return ternimal_menu.show()

def main(*args):
    # show options menu
    selected = show_options()
    # action. login or open tunnel
    action  = show_actions()
    
    switcher = {
        0:login,
        1:tunnet
    }
    switcher.get(action)(SSH_SERVER_CONFIGS[selected])



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass