import socket
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import matplotlib.pyplot as plt

KEY_SIZE = '1024'

# create a socket (connect two computers)
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


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global socket_criado

        print(f'Binding the Port {port}')

        server = (host, port)
        socket_criado.bind(server)
        socket_criado.listen(5)

    except socket.error as msg:
        print(f'Socket binding error:{str(msg)}\nRetrying...')
        bind_socket()

# Estabelecendo conexão com um cliente (socket deve ser escutado)
def socket_accept():
    conn, address = socket_criado.accept()
    print(f'Connection has been established! | IP {address[0]} | Port {str(address[1])}')
    handle(conn, address)
    conn.close()


# Função para criptografar usando chaves RSA retiradas da documentaçao da biblioteca cryptography
def criptografar(msg):
    #importar a chave de um arquivo
    key = RSA.importKey(open('public' + KEY_SIZE + '.pem').read())
    #cria uma cifra baseada na chave
    cipher = PKCS1_OAEP.new(key)
    #criptografa o texto que foi tranformado em bytes usando a ISO-8859-1
    ciphertext = cipher.encrypt(msg.encode('utf-8'))
    return ciphertext


# Função que transforma um texto em um binário
def text_to_binary(message):
    binary_message = ""

    for char in message:
        binary_char = bin(ord(char))[2:].zfill(8)  # Converte o caractere em um binário de 8 bits
        binary_message += binary_char

    return binary_message


# Função que aplica o algoritmo AMI em uma mensagem
def AMI(message):
    bits_msg = text_to_binary(message)
    lista_msg = []
    encoded_msg = []
    lista_msg = bits_msg
    polaridade = 1
    for bit in lista_msg:
        if bit == 0:
            encoded_msg.append(0) 
        else:
            encoded_msg.append(polaridade)
            polaridade = polaridade*(-1)
    return encoded_msg       


def plot_signal(signal, encoded_signal):
    list_signal = list(signal)
    plt.subplot(2, 1, 1)
    plt.plot(list_signal)
    plt.title('Original Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    plt.subplot(2, 1, 2)
    plt.plot(encoded_signal)
    plt.title('AMI Encoded Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    plt.tight_layout()
    plt.show()
    
def handle(conn, addr):
    msg = input("Mensagem a ser enviada: ")
    print("Mensagem pura: " + str(msg) + '\n' + "-----------------------------------------------", end='\n\n')
    msg = criptografar(msg)
    print("Mensagem criptografada: " + str(msg) + '\n' + "--------------------------------------", end='\n\n')
    msg = AMI(msg)
    print("Mensagem codificada: " + str(msg) + '\n' + "-----------------------------------------", end='\n\n')
    
    # Transforma o sinal pós-AMI em bytes para ser enviado pelo socket
    arr = msg[0].to_bytes(1, byteorder="big", signed=True)
    for i in range(1, len(msg)):
        arr+=msg[i].to_bytes(1, byteorder="big", signed=True)
    print("Mensagem em bytes: " + str(arr))
    
    # Envia a mensagem
    conn.send(arr)
        

def main():
    create_socket()
    bind_socket()
    socket_accept() 
    
if __name__ == "__main__":
    main()