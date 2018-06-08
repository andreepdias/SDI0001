import socketserver
from sys import argv

if len(argv) < 2:
	print("Tente: %s <server_port>" %argv[0])
	exit()

SERVERIP, SERVERPORT = "localhost", int(argv[1])

possuidores = []

class ConexaoTCP(socketserver.BaseRequestHandler):

	def handle(self):
		self.data = self.request.recv(1024).strip()
		print("%s solicitou:" % self.client_address[0])

		dados = str(self.data)
		dados = dados.split(";")
		dados[2] = dados[2][0:-1]
		print(dados)

		envio = ""

		if(dados[1] == "0"):
			#o cliente mandou uma mensagem nova, adiciona-o como possuidor da mesma na lista de possuidores
			possuidores.append(str(self.client_address[0]))
			envio = str(len(possuidores) - 1)
		if(dados[1] == "1"):
			#o cliente quer saber quem possui a mensagem com o índice contido em dados[2]
			envio = str(possuidores[int(dados[2])])
		if(dados[1] == "2"):
			# o cliente está informando que possui a mensagem com o índice contido em dados[2]
			possuidores[int(dados[2])] += ";" + str(self.client_address[0])
		if(dados[1] == "3"):
			 # o cliente está requisitando o total de mensagens
			envio = str(len(possuidores))
		self.request.sendall(bytes(envio, "utf-8"))

if __name__ == "__main__":
	try:
		server = socketserver.TCPServer((SERVERIP, SERVERPORT), ConexaoTCP)
		server.serve_forever()
	except KeyboardInterrupt:
		print("Stopping server")
	finally:
		server.server_close()
