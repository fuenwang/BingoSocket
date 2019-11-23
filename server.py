import sys
import time
import socket
import pickle
import numpy as np
from struct import pack, unpack
from myshare import MySend, MyRecv
from termcolor import colored, cprint

def CheckWinner(M):
    [h, w] = M.shape
    assert h == w
    count = 0
    # left to right
    for i in range(h):
        if not (M[:, i] != -1).any():
            count += 1
    # up to down
    for i in range(h):
        if not (M[i, :] != -1).any():
            count += 1
    # diag
    a = np.diag(M)
    if not (a != -1).any():
        count += 1
    a = np.diag(np.fliplr(M))
    if not (a != -1).any():
        count += 1

    return count

def GetStr(M, m=0):
    s = ''
    #s += '--------------------\n'
    [h, w] = M.shape
    for i in range(h):
        for j in range(w):
            if M[i, j] == -1:
                s += colored('  X ', 'red')
            else:
                if m == 0:
                    s += '%3d '%M[i, j]
                else:
                    s += '  O '
        s += '\n'
    #s += '--------------------'
    return s

def ChooseNum(sock):
    MySend(sock, 'c')
    num = MyRecv(sock)
    return num

def SendTurn(sock1, sock2, rounds, player1, player2):
    player1_score = CheckWinner(player1)
    player2_score = CheckWinner(player2)

    MySend(sock1, [rounds, player2_score, player1_score])
    MySend(sock1, GetStr(player2, 1))
    MySend(sock1, GetStr(player1, 0))

    MySend(sock2, [rounds, player1_score, player2_score])
    MySend(sock2, GetStr(player1, 1))
    MySend(sock2, GetStr(player2, 0))
    
    return player1_score, player2_score

def CheckWin(score1, score2):
    if score1 >= 3 or score2 >= 3:
        return True
    else:
        return False

if __name__ == '__main__':
    bind_ip = "140.114.27.221"
    bind_port = int(sys.argv[1])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(2)

    client_lst = []
    while len(client_lst) != 2:
        print ("Wait for player-%d" % (len(client_lst) + 1))
        client, addr = server.accept()
        print (addr)
        client_lst.append(client)

    player1, player2 = [MyRecv(client) for client in client_lst]
    #print (player1)
    #print (player2)
    sock1, sock2 = client_lst
    
    count = 1
    while True:
        MySend(sock2, 'w')
        num_1 = ChooseNum(sock1)
        player1[player1==num_1] = -1
        player2[player2==num_1] = -1 
        [player1_score, player2_score] = SendTurn(sock1, sock2, count, player1, player2)
        if CheckWin(player1_score, player2_score):
            print ('FINISH')
            break

        MySend(sock1, 'w')
        num_1 = ChooseNum(sock2)
        #print (num_1)
        player1[player1==num_1] = -1
        player2[player2==num_1] = -1
        
        [player2_score, player1_score] = SendTurn(sock2, sock1, count, player2, player1)
        if CheckWin(player1_score, player2_score):
            print ('FINISH')
            break


        count += 1
    sock1.close()
    sock2.close()
    server.close()
