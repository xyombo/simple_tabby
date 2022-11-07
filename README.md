# Simple Tabby

A hepler tool to manage many remote ssh server.

when you open a native terminal on unix system , stabby can list all remote ssh server that you have configed as a pretty table. Then you can choose one to login.

You will get more infomation about every remote ssh server depend on what's your describe for the server 

# Why

I just need a gadget for my work . In my work, i need to manage many remote server machines that deployed some application, such as java application,mysql and so on.
when i decided to connect some machines, I spend a lot of time checking which applications are deployed on each server
it's making me miserable. Tabby has wonderful **Profiles & connections** feature, but there no space to remark more information
for every machine or connection. I still need another document to manage information that can not hold with Tabby.

# Install

```shell
pip install stabby
```

# Usage

```shell

usage: stabby [-h] [-ls] [-c CONNECT] [-t TUNNET]

Hello

optional arguments:
  -h, --help            show this help message and exit
  -ls, --list           list all configed servers.
  -c CONNECT, --connect CONNECT
                        connect to remote server by No.
  -t TUNNET, --tunnet TUNNET
                        open tunnet with ssh localport:remoteport
```

# How does it work

It's so easy. Default , stabby(simple_tabby) loads config file under `$USER_HOME/.simple_tabby/terminals_config.json`, file content like below:

```json
[
  {
    "name": "name",
    "host": "remote server ip or host",
    "port": 22,
    "user": "remote user",
    "password": "remote password",
    "privateKey": "ssh key path",
    "describe": "description for the configuration",
    "application": [
      "first app that deploy in server",
      "second app that deploy in server"
    ],
    "tags": [
      "prod",
      "application-server"
    ]
  }
]
```

and the file need to create by yourself. you can use different json file to group your remote server information. if load file success, stabby will print as table like below:

| no  | name         | ip        | apps    | tags        | description         |
|-----|--------------|-----------|---------|-------------|---------------------|
| 1   | mysql-server | 127.0.0.1 | mysql   | mysql       | mysql machine       |
| 2   | spring-boot  | 127.0.0.2 | jar     | application | application machine |
| 3   | jenkins      | 127.0.0.3 | jenkins | devops      | ops machine         |


