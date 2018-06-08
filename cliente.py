import socket
import sys
import socketserver
import os
from sys import argv

if len(argv) < 2:
	print("Tente: %s <server_port>" %argv[0])
	exit()

SERVERIP, SERVERPORT = "localhost", int(argv[1])

nome = ""
msg_atual = ""
mensagens_conhecidas = 0
id_mensagem = 0
mensagens = [""] * 100

def mandaNovaMensagem(nome, texto):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((SERVERIP, SERVERPORT))
		envio = ";0;" + "<" + nome + ">:" + texto
		sock.sendall(bytes(envio, "utf-8"))
		recebido = str(sock.recv(1024), "utf-8")
	finally:
		sock.close()
	return int(recebido)

def requisicaoTotalMensagens():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((SERVERIP, SERVERPORT))
		envio = ";3;"
		sock.sendall(bytes(envio, "utf-8"))
		recebido = str(sock.recv(1024), "utf-8")
	finally:
		sock.close()
	return int(recebido)

def requestPossuidoresMensagem(indice):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((SERVERIP, SERVERPORT))
		envio = ";1;" + str(indice)
		sock.sendall(bytes(envio, "utf-8"))
		recebido = str(sock.recv(1024), "utf-8")
	finally:
		sock.close()
	return recebido

def requestMensagem(IPDESTINO, indice):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((IPDESTINO, 8888))
		envio = ";1;" + str(indice)
		sock.sendall(bytes(envio, "utf-8"))
		recebido = str(sock.recv(1024), "utf-8")
	finally:
		sock.close()
	return recebido


if __name__ == "__main__":
	print("Digite seu nome:")
	nome = input()
	escolha = ""
	while escolha != "/sair":
		# os.system("clear")
		if(id_mensagem > mensagens_conhecidas):
			print("***Você possui novas mensagens não lidas***")
		print("1 - mandar mensagem\n2 - receber mensagens\nEscolha uma opção: ")
		escolha = input()
		if(escolha == "1"):
			msg_atual = input()
			id_mensagem = mandaNovaMensagem(nome, msg_atual)
			if(id_mensagem == mensagens_conhecidas):
				mensagens_conhecidas += 1
			mensagens[id_mensagem] = msg_atual
		if(escolha == "2"):
			total_mensagens = requisicaoTotalMensagens()
			for i in range(mensagens_conhecidas, total_mensagens):
				if(mensagens[i] == ""):
					possuidores = split(requestPossuidoresMensagem(i), ";")
					mensagens[i] = requestMensagem(possuidores[0], i)
