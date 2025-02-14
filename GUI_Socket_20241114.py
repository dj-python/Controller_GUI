import socket

guiSocket = None

def init(ipAddress: str, portNumber: int) -> None:
    global guiSocket
    guiSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    guiSocket.setblocking(False)
    guiSocket.bind((ipAddress, portNumber))

def readMessage():
    global guiSocket

    try :
        return guiSocket.recvfrom(1024)
    except OSError:
        return None, None

def sendMessage(msg: str, target: tuple) -> None:
    global guiSocket
    guiSocket.sendto(msg.encode(), target)

v
