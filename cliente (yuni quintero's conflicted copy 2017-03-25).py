from pathlib import Path
from cancion import Cancion
from reproductor import Reproductor
from lista import ListaReproduccion, NodoLista
from PyQt5.QtWidgets import *
from arrayT import ArrayT
from cancion import Cancion

import sys
import subprocess as sp

if __name__ == "__main__":
	app = QApplication(sys.argv)
	try:
		archivo = sys.argv[1]
	except:
		archivo = 'canciones/canciones.txt'
	rep = Reproductor()
	rep.show()
	sp.call('clear', shell=True)
	with open(archivo, 'r') as f:
		lineas = f.readlines()
		n = len(lineas) - 1
		lista_de_reproduccion = ArrayT(n)
		for i in range(n):
			linea = lineas[i+1].split('\t')
			lista_de_reproduccion[i] = Cancion(linea[0], linea[1], linea[2][0:len(linea[2]) - 1])
			rep.sonarDespues(Cancion(linea[1], linea[0], linea[2][0:len(linea[2]) - 1]))

	#############
	# Menu loop #
	#############
	while True:
		print("1-Listar canciones")
		print("2-Agregar para sonar justo despues de la cancion actual")
		print("3-Agregar para sonar justo antes de la cancion actual")
		print("4-Ordenar lista de reproduccion por artista")
		print("5-Ordenar lista de reproduccion por titulo")
		print("6-Eliminar cancion por titulo")
		print("7-Mostrar opciones")
		print("8-Salir")
		op = int(input("Escoja una opcion: "))
		if op == 1:
			sp.call('clear', shell=True)
			rep.mostrar()
			t = 0
			input("presione ENTER para continuar.")
		elif op == 2:
			titulo = input("Ingrese el titulo de su cancion: ")
			artista = input("Ingrese el artista: ")
			direccion = input("Ingrese la direccion de su cancion: ")
			rep.sonarDespues(Cancion(titulo, artista, direccion))
		elif op == 3:
			titulo = input("Ingrese el titulo de su cancion: ")
			artista = input("Ingrese el artista: ")
			direccion = input("Ingrese la direccion de su cancion: ")
			rep.sonarAntes(Cancion(titulo, artista, direccion))
		elif op == 4:
			rep.ordenar_por_artista()
		elif op == 5:
			rep.ordenar_por_titulo()
		elif op == 6:
			titulo = input("Ingrese el titulo de la cancion a eliminar: ")
			song = ListaReproduccion()
			if rep.getSong() == titulo:
				print("qlq")
			rep.eliminar(titulo)
		elif op == 7:
			pass
		elif op == 8:
			choice = input("¿Estas seguro? (si/no): ")
			if choice == "si":
				sys.exit(0)
			else:
				sp.call('clear', shell=True)
				continue
		else:
			pass
		sp.call('clear', shell=True)

	# Para eliminar una canción debe solicitar el título y pasarlo al método
	# eleminar de la instancia de Reproductor 'rep'.
	# 
	# rep.eliminar(titulo_solicitado)

	############
	# Fin menu #
	############

	sys.exit(app.exec_())