
import argparse
import os
import json
import pyperclip
import sys
import paramiko
import select
import termios
import tty
from simple_tabby import inactive

__version_info__ = (1, 0, 6)
__version__ = ".".join(map(str, __version_info__))


DEFAULT_SHELL_TERM="linux"
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.simple_tabby")
SSH_SERVER_CONFIGS = []

  
def show_options():
    load_config()
    from simple_term_menu import TerminalMenu
    options = [SSH_SERVER_CONFIGS[i]['title'] for i in range(len(SSH_SERVER_CONFIGS))]
    ternimal_menu = TerminalMenu(options,show_search_hint=True,quit_keys=["q"],preview_command=pc, preview_size=0.75)
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

def add(args):
    load_config()
    SSH_SERVER_CONFIGS.append({
        'title':args.n if args.n else args.s,
        'host':args.s,
        'user':args.u,
        'password':args.p,
        'port':args.port
    })
    save_file()

def delConfig(args):
    selected_idx = show_options()
    if(selected_idx is not None):
        del SSH_SERVER_CONFIGS[selected_idx:selected_idx+1]
        save_file()
    
    
def main():
    # default command
    parser = argparse.ArgumentParser(description="Mini tool login remote ssh server ", add_help=True)
    parser.add_argument('-t', '--tunnet', type=str, required=False,nargs='?',
                    help="open tunnet with ssh localport:remoteport")
    parser.set_defaults(func=inactive.main)
    
    #sub command to add new server
    subparsers = parser.add_subparsers(help='sub-command help')
    add_parser = subparsers.add_parser('add',help="add new server config")
    add_parser.add_argument('-s',type=str,required=True,help="remote server host")
    add_parser.add_argument('-p',type=str,required=False,help="remote server password")
    add_parser.add_argument('-port',type=int,default=22,help="remote server ssh port")
    add_parser.add_argument('-u',type=str,default="root",help="remote server user name ")
    add_parser.add_argument('-n',type=str,default=None,help="remote server name ")
    add_parser.set_defaults(func=add)

    # sub command to delete server
    del_parser = subparsers.add_parser("del",help="delete server config")
    del_parser.set_defaults(func=delConfig)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass