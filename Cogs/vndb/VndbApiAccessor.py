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


def requestVnData(id = None, title = None, flags = "basic,details,stats"):
    try:
        if id is not None:
            requeststring = "get vn {0} (id={1})\x04".format(flags, id)
        elif title is not None:
            requeststring = "get vn {0} (search~\"{1}\")\x04".format(flags, title)
        else:
            #maybe at some point add other ways to search, for now just terminate
            return None
        ssock.send(bytes(requeststring,"utf-8"))
        response=ssock.recv(16384)
        return response[8:-1]     #API response includes string in front of the JSON object, remove that as well as the trailing \x04
    except Exception as e:
        print("Requesting VN failed, error: {0}".format(e))