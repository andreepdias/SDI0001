import os
import sys
import time
import socket
import socketserver
import _thread as thread
from sys import argv

if len(argv) < 3:
	print("Tente: %s <server_port> <client_port>" %argv[0])
	exit()

SERVERIP, SERVERPORT = "localhost", int(argv[1])
CLIENTIP, CLIENTPORT = "localhost", int(argv[2])

mensagens = {}
numero_indices_conhecidos = 0

def clearScreen():
	os.system('cls' if os.name == 'nt' else 'clear')

def requisaoNovoIndice():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((SERVERIP, SERVERPORT))
		envio = ";0;" + str(CLIENTPORT) + ";"
		sock.sendall(bytes(envio, "utf-8"))
		recebido = str(sock.recv(1024), "utf-8")
	finally:
		sock.close()
	return int(recebido)

def requisicaoPossuidoresMensagem(indice):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((SERVERIP, SERVERPORT))
		envio = ";1;" + str(indice) + ";" + str(CLIENTPORT) + ";"
		sock.sendall(bytes(envio, "utf-8"))
		recebido = str(sock.recv(1024), "utf-8")
	finally:
		sock.close()
		return recebido

def enviaAquisicaoIndice(indice):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((SERVERIP, SERVERPORT))
		envio = ";2;" + str(indice) + ";" + str(CLIENTPORT) + ";"
		sock.sendall(bytes(envio, "utf-8"))
		recebido = str(sock.recv(1024), "utf-8")
	finally:
		sock.close()
		return recebido

def requisicaoTotalMensagens():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((SERVERIP, SERVERPORT))
		envio = ";3;" + str(CLIENTPORT) + ";"
		sock.sendall(bytes(envio, "utf-8"))
		recebido = str(sock.recv(1024), "utf-8")
	finally:
		sock.close()
	return int(recebido)

def requisicaoMensagem(indice, ip, porta):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	recebido = ""
	try:
		sock.connect((ip, int(porta)))
		envio = ";" + str(indice) + ";"
		sock.sendall(bytes(envio, "utf-8"))
		recebido = str(sock.recv(1024), "utf-8")
	except socket.error:
		sock.close()
	finally:
		sock.close()
	return recebido

def escreverMensagem(mensagem):
	global mensagens
	id = requisaoNovoIndice()
	mensagens[id] = "[" + nome + "] : " + mensagem

def receberMensagens():
	global numero_indices_conhecidos
	global mensagens
	total = requisicaoTotalMensagens()
	mensagem = ""
	a = numero_indices_conhecidos + 1
	b = total + 1
	for i in range(a, b):
		if not (i in mensagens):
			possuidores = requisicaoPossuidoresMensagem(i)
			possuidores = possuidores.split(";")
			c = len(possuidores) - 1
			for j in range(0, c):
				possuidor = possuidores[j].split(":")
				ip = possuidor[0]
				porta = possuidor[1]
				msg = ""
				msg = requisicaoMensagem(i, ip, porta)
				if(msg != ""):
					mensagem += msg + "\n"
					mensagens[i] = msg
					enviaAquisicaoIndice(i)
	return mensagem

def threadAguardaSolicitacoes():
	try:
		server = socketserver.TCPServer((CLIENTIP, CLIENTPORT), ConexaoTCP)
		server.serve_forever()
	except KeyboardInterrupt:
		print("Stopping server")
	finally:
		server.server_close()

class ConexaoTCP(socketserver.BaseRequestHandler):

	def handle(self):
		self.data = self.request.recv(1024).strip()

		dados = str(self.data)
		dados = dados.split(";")

		indice = dados[1]

		envio = mensagens[int(indice)]
		self.request.sendall(bytes(envio, "utf-8"))

def threadRecebeMensagens():
	while(True):
		msg = receberMensagens()
		if(msg != ""):
			print(msg)
		time.sleep(1)

if __name__ == "__main__":
	thread.start_new_thread(threadAguardaSolicitacoes, ())

	clearScreen()
	global nome
	print("Digite seu nome:")
	nome = input()

	mensagem = ""

	numero_indices_conhecidos = requisicaoTotalMensagens()

	clearScreen()
	print("Bem-vindo ao Chat P2P, " + nome + "!\t(" + str(CLIENTPORT) + ")\n")
	print("(digite /sair para se retirar do chat)\n")

	thread.start_new_thread(threadRecebeMensagens, ())
	while mensagem != "/sair":
		mensagem = input()
		escreverMensagem(mensagem)
