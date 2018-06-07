#!/usr/sbin/python3
#! coding=utf-8

import socketserver
import sys

# armazena id do avião, num_parada, latitute, longitude, carga
avioes = {}
contador = 0
HOST = ""
PORT = ""

class MyTCPHandler(socketserver.BaseRequestHandler):

	def handle(self):
		global contador
		self.data = self.request.recv(1024).strip()
		data = str(self.data)
		data = data.split(";")

		print("Recebido de %s: %s" %(self.client_address[0], data))

		if(data[1] == "0"):  #Guarda dados
			#paradas.append([data[2], data[3], data[4], data[5], data[6]])
			# Recebe no formato: "x;0;<id_aviao>;<latitude>;<longitude>;<carga_descarga>;x"
			if not data[2] in avioes:
				avioes[data[2]] = []
			id_parada = len(avioes[data[2]])
			avioes[data[2]].append((contador, id_parada, data[3], data[4], data[5]))
			contador += 1
			self.request.sendall(bytes("DADOS RECEBIDOS", "utf-8"))

		if(data[1] == "1"): #Envia dados
			'''
			Considerando que o request seja no formato 'x;1;n;x', onde n é o
				índice do próximo registro que o cliente_framebuffer espera
			Envio limitado a 10 registros por solicitação, para não sobrecarregar
				o buffer de envio.
			'''
			c = 0
			i = 0
			envio = ""
			for a in avioes:
				if c > 10:
					break
				for p in avioes[a]:
					if c > 10:
						break
					if(p[0] >= int(data[2])):
						envio += str(a + " " + str(p[0]) + " " + str(p[1]) + " " + p[2] +
							" " + p[3] + " " + p[4] + "\n")
						c += 1
			print("Enviando %s" %envio);
			self.request.sendall(bytes(envio, "utf-8"))

if __name__ == "__main__":
	PORT = 9998
	#print("Digite o endereco do servidor: ")
	# Ouvir em todos endereços locais
	HOST = '0.0.0.0'

	print("Iniciando servidor")
	try:
		# Create the server, binding to localhost on port 9990
		server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

		# Activate the server; this will keep running until you
		# interrupt the program with Ctrl-C
		server.serve_forever()
	except KeyboardInterrupt:
		print("Stopping server")
	finally:
		server.server_close()
