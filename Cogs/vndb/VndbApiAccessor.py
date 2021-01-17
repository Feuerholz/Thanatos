import socket
import ssl
import json

hostname="api.vndb.org"
port="19535"
context = ssl.create_default_context()


def login():

    global sock
    sock = socket.create_connection((hostname, port))
    global ssock
    ssock = context.wrap_socket(sock, server_hostname=hostname)
    with open ("vndb.txt", "r") as credentials:
        lines = credentials.readlines()
        user = lines[0].replace('\n', '')
        pw = lines[1].replace('\n', '')
    logindata = {"protocol":1,"client":"Thanatos","clientver":1.0,"username": user,"password":pw}
    loginstring = "login " + json.dumps(logindata) + "\x04"
    print(loginstring)

def closeConnection():
    ssock.close()