
import argparse
import os
import json
import pyperclip
import sys
import paramiko
import select
import termios
import tty

__version_info__ = (1, 0, 5)
__version__ = ".".join(map(str, __version_info__))


DEFAULT_CONFIG_PATH = os.path.expanduser("~/.simple_tabby")
SSH_SERVER_CONFIGS = []

def open_session(host,user,port,passwrd):
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(1)
        client.connect(host,port=port,username=user)
        print(1)
        channel = client.invoke_shell(width=1000,height=500)
        oldtty = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        while True:
            readlist, writelist, errlist = select.select([channel, sys.stdin,], [], [])
            if sys.stdin in readlist:
                input_cmd = sys.stdin.read(1)
                channel.sendall(input_cmd)
            if channel in readlist:
                result = channel.recv(1024)
                if len(result) == 0:
                    break
                sys.stdout.write(result.decode())
                sys.stdout.flush()
    except Exception as err:
        print(str(err))
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
        channel.close() 
        client.close()
        print('\r\n*** stabby logout ***\r\n')


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
        print("-> run command :",command)
        i = os.system(command)
    else:
        open_session(host, user, port, passwd)


def pc(args):
    if args is not None:
        for config in SSH_SERVER_CONFIGS:
            if config['title']==args :
                return f"host:{config['host']} \nport:{config['port']}\nuser:{config['user']}\n"
    return None
   
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

def login(args):
    selected_idx = show_options()
    if(selected_idx is not None):
        selected_config = SSH_SERVER_CONFIGS[selected_idx]
        connect(selected_config,args)

def delConfig(args):
    selected_idx = show_options()
    if(selected_idx is not None):
        del SSH_SERVER_CONFIGS[selected_idx:selected_idx+1]
        save_file()
    
    
def main():
    parser = argparse.ArgumentParser(description="Mini tool login remote ssh server ", add_help=True)
    parser.add_argument('-t', '--tunnet', type=str, required=False,nargs='?',
                    help="open tunnet with ssh localport:remoteport")
    parser.set_defaults(func=login)
    
    subparsers = parser.add_subparsers(help='sub-command help')
    add_parser = subparsers.add_parser('add',help="add new server config")
    add_parser.add_argument('-s',type=str,required=True,help="remote server host")
    add_parser.add_argument('-p',type=str,required=False,help="remote server password")
    add_parser.add_argument('-port',type=int,default=22,help="remote server ssh port")
    add_parser.add_argument('-u',type=str,default="root",help="remote server user name ")
    add_parser.add_argument('-n',type=str,default=None,help="remote server name ")
    add_parser.set_defaults(func=add)

    del_parser = subparsers.add_parser("del",help="delete server config")
    del_parser.set_defaults(func=delConfig)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass