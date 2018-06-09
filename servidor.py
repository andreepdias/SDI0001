import os
import socketserver
from sys import argv

if len(argv) < 2:
	print("Tente: %s <server_port>" %argv[0])
	exit()

SERVERIP, SERVERPORT = "localhost", int(argv[1])

possuidores = {}
numero_indices = 0

def clearScreen():
	os.system('cls' if os.name == 'nt' else 'clear')

def appendIndice(indice, ip, porta):
	global possuidores
	possuidores[int(indice)].append((str(ip), str(porta)))

def novoIndice():
	global numero_indices
	global possuidores
	numero_indices += 1
	possuidores[numero_indices] = []
	return str(numero_indices)

def retornaPossuidores(indice):
	global possuidores
	p = ""
	indice = int(indice)
	for i in range(0, len(possuidores[indice])):
		p = p + str(possuidores[indice][i][0]) + ":" + str(possuidores[indice][i][1]) + ";"
	return p

class ConexaoTCP(socketserver.BaseRequestHandler):

	def handle(self):
		self.data = self.request.recv(1024).strip()

		dados = str(self.data)
		dados = dados.split(";")

		ip = str(self.client_address[0])

		if(len(dados) > 2):
			porta = dados[2]

		envio = ""

		if(dados[1] == "0"):
			#o cliente mandou uma mensagem nova, adiciona-o como possuidor da mesma na lista de possuidores
			indice = novoIndice()
			appendIndice(indice, ip, porta)
			envio = indice
			print("[0] Cliente " + ip + ":" + porta + " solicitou um novo índice (" + indice + ")")
		elif(dados[1] == "1"):
			#o cliente quer saber quem possui a mensagem com o índice contido em dados[2]
			indice = dados[2]
			envio = retornaPossuidores(indice)
			print("[1] Cliente " + ip + ":" + porta + " solicitou quem possui o índice (" + indice + ")")
		elif(dados[1] == "2"):
			# o cliente está informando que possui a mensagem com o índice contido em dados[2]
			indice = dados[2]
			ip = str(self.client_address[0])
			porta = dados[3]
			appendIndice(indice, ip, porta)
			print("[2] Cliente " + ip + ":" + porta + " agora possui o índice (" + indice + ")")
		elif(dados[1] == "3"):
			 # o cliente está requisitando o total de mensagens
			print("[3] Cliente " + ip + ":" + porta + " solicitou o total de índices (" + str(numero_indices) + ")")
			envio = str(numero_indices)
		self.request.sendall(bytes(envio, "utf-8"))

if __name__ == "__main__":
	clearScreen()
	print("Servidor iniciado na porta " + str(SERVERPORT) + ".")
	try:
		server = socketserver.TCPServer((SERVERIP, SERVERPORT), ConexaoTCP)
		server.serve_forever()
	except KeyboardInterrupt:
		print("Stopping server")
	finally:
		server.server_close()
