import socket
import ssl
import json

hostname="api.vndb.org"
port="19535"
context = ssl.create_default_context()


def login():
    try:
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
        ssock.send(bytes(loginstring, "utf-8"))
        response=ssock.recv(4096)
        print("login response: {0}".format(response))
    except Exception as e:
        print("error logging in, error: {0}".format(e))

def closeConnection():
    try:
        ssock.shutdown(socket.SHUT_RDWR)
        ssock.close()
        print ("socket closed successfully")
    except Exception as e:
        print("closing socket failed, error: {0}".format(e))


def requestVnData(id = None, flags = "basic"):
    try:
        requeststring = "get vn {0} (id={1})\x04".format(flags, id)
        ssock.send(bytes(requeststring,"utf-8"))
        response=ssock.recv(4096)
        print("VN Requested successfully, Response: {0}".format(response[8:][:-1]))
        return response[8:][:-1]     #API response includes string in front of the JSON object, remove that as well as the trailing \x04
    except Exception as e:
        print("Requesting VN failed, error: {0}".format(e))