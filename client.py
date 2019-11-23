import sys
import socket
import pickle
import numpy as np
from myshare import MyRecv, MySend
from termcolor import colored, cprint

N = 8

def GetTurn(sock):
    tmp = MyRecv(sock)
    [rounds, enemy, my] = tmp
    #[rounds, enemy, my] = MyRecv(sock)
    enemy_mat = MyRecv(sock)
    my_mat = MyRecv(sock)

    return [rounds, enemy, my], enemy_mat, my_mat

def Print(enemy, my, rounds, enemy_score, my_score):
    a = enemy.split('\n')
    b = my.split('\n')
    s = ''
    s += '------------  Round %d  --------------\n'%(rounds)
    s += 'You: %2d    Enemy: %2d\n\n'%(my_score, enemy_score)
    for e, m in zip(b, a):
        s += e + '                  ' + m + '\n'
    s += '--------------------------------------'
    print (s)

def CheckWin(you, enemy):
    if you >= 3:
        print ('You win !!')
        return True
    elif enemy >=3:
        print ('You lose !!')
        return True
    else:
        return False

if __name__ == '__main__':
    tgt_ip = "140.114.27.221"
    tgt_port = int(sys.argv[1])
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((tgt_ip, tgt_port))


    my_mat = np.random.choice(range(N*N), N*N, replace=False).reshape([N, N])

    print (my_mat)
    print ('=====================\n')
    MySend(client, my_mat) 
    while True:
        cmd = MyRecv(client)
        if cmd == 'c':
            num = int(input("Choose: "))
            MySend(client, num)
            [tmp, enemy_mat, my_mat] = GetTurn(client)
            [rounds, enemy_score, my_score] = tmp
            Print(enemy_mat, my_mat, rounds, enemy_score, my_score)
            if CheckWin(my_score, enemy_score):
                break
        elif cmd == 'w':
            print ('Wait~~~~~~~')
            [tmp, enemy_mat, my_mat] = GetTurn(client)
            [rounds, enemy_score, my_score] = tmp
            Print(enemy_mat, my_mat, rounds, enemy_score, my_score)
            if CheckWin(my_score, enemy_score):
                break

            num = int(input("Choose: "))
            if MyRecv(client) != 'c':
                print ('Error!!!')
                exit()
            MySend(client, num)
            [tmp, enemy_mat, my_mat] = GetTurn(client)
            [rounds, enemy_score, my_score] = tmp
            Print(enemy_mat, my_mat, rounds, enemy_score, my_score)
            if CheckWin(my_score, enemy_score):
                break

    client.close()
