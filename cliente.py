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
		print("Recuerde ingresar el archivo como argumento del programa.\nEj: python3 cliente.py <archivo>")
		sys.exit(1)
	rep = Reproductor()
	rep.show()
	sp.call('clear', shell=True)
	with open(archivo, 'r') as f:
		lineas = f.readlines()
		n = int(lineas[0][:len(lineas)-1])
		lista_de_reproduccion = ArrayT(n)
		for i in range(n):
			linea = lineas[i+1].split('\t')
			lista_de_reproduccion[i] = Cancion(linea[0], linea[1], linea[2][0:len(linea[2]) - 1])
			rep.sonarDespues(Cancion(linea[1], linea[0], linea[2][0:len(linea[2]) - 1]))

	conf = "\tPresione ***<ENTER> para cancelar la operacion"
	data = ArrayT(9)
	data[0] = "1-Listar canciones"
	data[1] = "2-Agregar para sonar justo despues de la cancion actual"
	data[2] = "3-Agregar para sonar justo antes de la cancion actual"
	data[3] = "4-Ordenar lista de reproduccion por artista"	
	data[4] = "5-Ordenar lista de reproduccion por titulo"
	data[5] = "6-Eliminar cancion por titulo"
	data[6] = "7-Mostrar opciones" 
	data[7] = "8-Salir"
	menu = "\n{:18}+{:-^61}+\n".format('\0', '-')
	menu += "                 | {0[0]:60}|\n                 | {0[1]:60}|\n                 \
| {0[2]:60}|\n                 | {0[3]:60}|\n                 | {0[4]:60}|\n                 \
| {0[5]:60}|\n                 | {0[6]:60}|\n                 | {0[7]:60}|\n".format(data)
	menu += "{:18}+{:-^61}+\n".format('\0', '-')

	print(menu)
	#############
	# Menu loop #
	#############
	while True:
		try:
			print("     {:-^25}".format('-'))
			op = int(input("\tEscoja una opcion: "))
			assert 1 <= op <= 8
			if op == 1:
				print("")
				rep.mostrar()
			elif op == 2:
				try:
					print(conf)
					titulo = input("\tIngrese el titulo de su cancion: ")
					assert(titulo != '***')
					artista = input("\tIngrese el artista: ")
					assert(artista != '***')
					direccion = input("\tIngrese la direccion de su cancion: ")
					assert(direccion != '***')
					rep.sonarDespues(Cancion(titulo, artista, direccion))
				except:
					print("\tOperacion cancelada.")
					pass
			elif op == 3:
				try:
					print(conf)
					titulo = input("\tIngrese el titulo de su cancion: ")
					assert(titulo != '***')
					artista = input("\tIngrese el artista: ")
					assert(artista != '***')
					direccion = input("\tIngrese la direccion de su cancion: ")
					assert(direccion != '***')
					rep.sonarAntes(Cancion(titulo, artista, direccion))
				except:
					print("\tOperacion cancelada.")
					pass
			elif op == 4:
				rep.ordenar_por_artista()
				print("\tLista ordenada por artista.")
			elif op == 5:
				rep.ordenar_por_titulo()
				print("\tLista ordenada por titulo.")
			elif op == 6:
				try:
					print(conf)
					titulo = input("\tIngrese el titulo de la cancion a eliminar: ")
					assert(titulo != '***')
					rep.eliminar(titulo)
				except:
					print("\tOperacion cancelada.")
					pass
			elif op == 7:
				print(menu)
			elif op == 8:
				choice = input("\t¿Estas seguro? (si/no): ").lower()
				if choice == "si":
					sys.exit(0)
				else:
					pass
		except AssertionError:
			print("\tAsegurese de ingresar un numero entre 1 y 8 (ambos inclusive)")
		except ValueError:
			print("\tIngreso un caracter no valido")

	# Para eliminar una canción debe solicitar el título y pasarlo al método
	# eleminar de la instancia de Reproductor 'rep'.
	# 
	# rep.eliminar(titulo_solicitado)

	############
	# Fin menu #
	############

	sys.exit(app.exec_())
