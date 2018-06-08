import socketserver
from sys import argv

if len(argv) < 2:
	print("Tente: %s <server_port>" %argv[0])
	exit()

SERVERIP, SERVERPORT = "localhost", int(argv[1])

numero_indices = 0

class ConexaoTCP(socketserver.BaseRequestHandler):

	def handle(self):
		self.data = self.request.recv(1024).strip()
		print("%s solicitou:" % self.client_address[0])

		dados = str(self.data)
		dados = dados.split(";")
		print(dados[1])

		envio = ""

		if(dados[1] == "0"):
			envio = str(numero_indices)

		self.request.sendall(bytes(envio, "utf-8"))

if __name__ == "__main__":
    try:
        server = socketserver.TCPServer((SERVERIP, SERVERPORT), ConexaoTCP)
        server.serve_forever()
    except KeyboardInterrupt:
    	print("Stopping server")
    finally:
    	server.server_close()
