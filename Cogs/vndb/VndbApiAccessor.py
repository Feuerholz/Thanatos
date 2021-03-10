import socket
import ssl
import json
import logging
logger = logging.getLogger()
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
        logger.info("login response: {0}".format(response))
    except Exception as e:
        logger.error("error logging in: {0}".format(e))

def closeConnection():
    try:
        ssock.shutdown(socket.SHUT_RDWR)
        ssock.close()
        logger.info("socket closed successfully")
    except Exception as e:
        logger.error("closing socket failed: {0}".format(e))


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
        response=ssock.recv(65536)
        logger.info("VN Data for query \"{0}\" requested successfully, response: {1}".format(requeststring, response))
        return response[8:-1]     #API response includes string in front of the JSON object, remove that as well as the trailing \x04
    except Exception as e:
        logger.error("Requesting VN failed: {0}".format(e))