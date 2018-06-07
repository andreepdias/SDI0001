#!/usr/sbin/python3
#! coding=utf-8

import socket
import sys
from sys import argv
import time
from random import randrange, uniform

PORT = 9998
HOST = ""

#print("Digite o IP do servidor")
if len(argv) < 2:
	print("Uso: %s <ip_servidor>" %argv[0])
	exit()

HOST = argv[1];

while True:
	try:
		print("Digite o numero do aviao: ")
		num_aviao = int(input())
		while True:
			print("Digite a latitude: ")
			lat = float(input())
			if(not (lat > 90 or lat < -90)):
				break
			print("Latitude deve estar entre -90 e 90, tente novamente.")

		while True:
			print("Digite a longitude: ")
			long = float(input())
			if(not (long > 180 or long <= -180)):
				break
			print("Longitude deve estar entre -180 e 180, tente novamente.")

		print("Digite qual alteração na carga (positivo para carga e negativo para descarga): ")
		carga = float(input())
		data = "x;0;" + str(num_aviao) + ";" + str(lat) + ";" + str(long) + ";" + str(carga) + ";x"

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		sock.sendall(bytes(data, "utf-8"))
		received = str(sock.recv(1024), "utf-8")
	finally:
		sock.close()
	print("Sent:	 %s" % data)
	print("Received: %s" % received)
	time.sleep(1)
