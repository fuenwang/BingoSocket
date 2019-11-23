import time
import socket
import pickle
import numpy as np
from struct import pack, unpack

def MySend(sock, data):
    data_str = pickle.dumps(data)
    sock.sendall(pack('<I', len(data_str)))
    sock.sendall(bytes(data_str))

def MyRecv(sock):
    data = b''
    while len(data) < 4:
        packet = sock.recv(4 - len(data))
        if not packet: return None
        data += packet
    total = unpack('I', data)[0]
    data = b''
    while len(data) < total:
        packet = sock.recv(total - len(data))
        if not packet:
            return None
        data += packet
    #data = data.decode('utf8')
    data = pickle.loads(data, encoding='bytes')
    return data

