import socket
import sys
import socketserver
from sys import argv

if len(argv) < 2:
	print("Tente: %s <server_port>" %argv[0])
	exit()

SERVERIP, SERVERPORT = "localhost", int(argv[1])

nome = ""
numero_indices = 0

def solicitaNumeroIndices():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVERIP, SERVERPORT))
        envio = ";0" + ";" + "\n";
        sock.sendall(bytes(envio, "utf-8"))
        recebido = str(sock.recv(1024), "utf-8")
    finally:
        sock.close()
    return int(recebido)

if __name__ == "__main__":
    print ("Digite seu nome:")
    nome = input()

    numero_indices = solicitaNumeroIndices()

    print (numero_indices)
