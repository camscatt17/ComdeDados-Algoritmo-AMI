import socket
import matplotlib.pyplot as plt
import numpy as np
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

KEY_SIZE = '1024'
SIGNAL = 2

def create_socket():
    try:
        global host
        global port
        global socket_criado

        host = '192.168.0.162'
        port = 9999
        socket_criado = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as msg:
        print(f'Socket creation error:{str(msg)}')

def connect_socket():
    server = (host, port)
    socket_criado.connect(server)
    
def descriptografar(msg):
    key = RSA.importKey(open('private' + KEY_SIZE + '.pem').read())
    #Cria uma cifra usando essa chave
    cipher = PKCS1_OAEP.new(key)
    #Decodifica a mensagem usando a cifra
    return cipher.decrypt(msg)


# Remove o hifen de uma lista, substituindo-o por um espaço vazio e depois o retirando desta lista
def remove_hifen(list_signal):
    new_list = []
    for item in list_signal:
        item_signal = item.replace("-","")
        new_list.append(item_signal)
    new_list.remove("")
    return new_list


# Função que decodifica o algoritmo AMI
def decode_AMI(message):
    encoded_msg = []
    for bit in message:
        if bit == '0':
            encoded_msg.append(0) 
        else:
            encoded_msg.append(1)
    return encoded_msg         


def plot_signal(signal, dencoded_signal):
    list_signal = list(signal)
    plt.subplot(2, 1, 1)
    plt.plot(list_signal)
    plt.title('Original Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    plt.subplot(2, 1, 2)
    plt.plot(dencoded_signal)
    plt.title('AMI Encoded Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    plt.tight_layout()
    plt.show()
    
# Função para converter uma string de bits para bytes
def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])  

def mensagem():
    msg = socket_criado.recv(2048)
    print("Mensagem recebida: " + str(msg) + '\n' + "--------------------------------------------------------------------------------------------------", end='\n\n')
    msg = decode_AMI(msg)
    arr = ''.join(str(x) for x in msg)
    arr = '0b' + arr
    print("Mensagem pós-AMI: " + str(arr) + '\n' + "--------------------------------------------------------------------------------------------------", end='\n\n')
    msg = bitstring_to_bytes(arr)
    print("Mensagem em bytes: " + str(msg) + '\n' + "--------------------------------------------------------------------------------------------------", end='\n\n')
    msg = descriptografar(msg)
    print("Mensagem descriptografada: " + str(msg) + '\n' + "--------------------------------------------------------------------------------------------------", end='\n\n')
    msg = msg.decode('utf-8')
    print("Mensagem traduzida: " + str(msg))  

def main():
    create_socket()
    connect_socket()
    mensagem()
    
if __name__ == '__main__':
    main()