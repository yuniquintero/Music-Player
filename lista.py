from cancion import Cancion
from arrayT import ArrayT

class NodoLista():
	def __init__(self, e, s, a):
		self.elemento = e
		self.siguiente = s
		self.anterior = a

	def __str__(self):
		string = self.elemento.__str__()
		return string

	def __repr__(self):
		return self.__str__()

class ListaReproduccion():

	#################################################
	#												#
	#			  Inicializacion y metodos:			#
	#												#
	#################################################

	def __init__(self):
		self.proxima = None
		self.numero_nodos = 0

	def mostrar(self):
		separador = "                 +------------------------------+------------------------------+\n"
		string = separador
		string += " {:17s}| {:^59} |\n".format('\0'," Playlist Actual ")
		string += separador
		string += "{:s}|{:^30s}|{:^30s}|\n".format("                 ", "Titulo", "Artista", "-")
		string += separador 
		aux = self.proxima
		i = 0
		while i < self.numero_nodos:
			if i == 0:
				string += "Proxima Cancion: "
			elif i == self.numero_nodos -1:
				string += "Cancion Actual:  "
			else:
				string += "                 "
			string += aux.__str__()
			aux = aux.siguiente
			i += 1
			string = string + '\n'
			if i == self.numero_nodos - 1:
				string += separador
		string += separador
		print(string)

	def is_empty(self):
		return self.numero_nodos == 0


	def agregar_final(self,e):
		if self.is_empty():
			self.proxima = NodoLista(e, None, None)
			self.proxima.siguiente = self.proxima
			self.proxima.anterior = self.proxima
			self.numero_nodos += 1
			return
		e = NodoLista(e, None, None)
		if self.buscar(e) != None:
			print("Esa cancion ya esta en la lista de reproduccion.")
			return
		nex = self.proxima
		actual = self.proxima.anterior
		e.siguiente = nex
		e.anterior = actual
		actual.siguiente = e
		nex.anterior = e
		self.numero_nodos += 1

	def buscar(self, e):
		aux = self.proxima
		i = 0
		while i < self.numero_nodos:
			if e.elemento.es_igual(aux.elemento):
				return aux
			aux = aux.siguiente
			i += 1
		return None

	def agregar(self,e):
		if self.is_empty():
			self.proxima = NodoLista(e, None, None)
			self.proxima.siguiente = self.proxima
			self.proxima.anterior = self.proxima
			self.numero_nodos += 1
			return True
		e = NodoLista(e, None, None)
		if self.buscar(e) != None:
			print("\tEsa cancion ya esta en la lista de reproduccion.")
			return
		proxima = self.proxima
		actual = self.proxima.anterior
		e.siguiente = proxima
		e.anterior = actual
		actual.siguiente = e
		proxima.anterior = e
		self.proxima = e
		self.numero_nodos += 1
		

	def eliminar(self,tituloCancion, n = 0):
		if n == 0:
			aux = self.proxima
			i = 0
			while i < self.numero_nodos:
				if aux.elemento.titulo == tituloCancion:
					sucesor = aux.siguiente
					predecesor = aux.anterior
					predecesor.siguiente = sucesor
					sucesor.anterior = predecesor
					if aux.elemento.es_igual(self.proxima.elemento):
						self.proxima = sucesor
					del aux
					self.numero_nodos -= 1
					print("\tCancion eliminada.")
					return
				i += 1
				aux = aux.siguiente
			print("\tLa cancion no se encuentra en la lista de reproducion")
		else:
			aux = self.proxima.siguiente
			ret = NodoLista(self.proxima.siguiente.elemento, None, None)
			sucesor = aux.siguiente
			predecesor = aux.anterior
			predecesor.siguiente = sucesor
			sucesor.anterior = predecesor
			self.proxima = predecesor
			self.numero_nodos -= 1
			return ret
	
	#################################################
	#												#
	#			   Parte de ordenamiento			#
	#												#
	#################################################

	def append(self, e):
		if self.is_empty():
			self.proxima = e
			self.proxima.siguiente = self.proxima
			self.proxima.anterior = self.proxima
			self.numero_nodos += 1
			return
		sucesor = self.proxima.siguiente
		predecesor = self.proxima
		e.anterior = predecesor
		e.siguiente = sucesor
		predecesor.siguiente = e
		sucesor.anterior = e
		self.proxima = e
		self.numero_nodos += 1

	def dividirEnDos(self, l, r):
		while not self.is_empty():
			l.append(self.eliminar("", n = 1))
			if self.is_empty(): break
			r.append(self.eliminar("", n = 1))

	def merge(self, l, r, tipo):
		while not l.is_empty() and not r.is_empty():
			if tipo == 'titulo':
				if l.proxima.siguiente.elemento.es_menor_titulo(r.proxima.siguiente.elemento):
					self.append(l.eliminar("", n = 1))
				else:
					self.append(r.eliminar("", n = 1))
			else:
				if l.proxima.siguiente.elemento.es_menor_artista(r.proxima.siguiente.elemento):
					self.append(l.eliminar("", n = 1))
				else:
					self.append(r.eliminar("", n = 1))
		while not l.is_empty():
			self.append(l.eliminar("", n = 1))
		while not r.is_empty():
			self.append(r.eliminar("", n = 1))

	def merge_sort(self, tipo, depth = 1):
		if self.is_empty() or self.numero_nodos == 1:
			return
		q = self.numero_nodos // 2
		aux = self.proxima
		l, r = ListaReproduccion(), ListaReproduccion()
		self.dividirEnDos(l, r)
		l.merge_sort(tipo, depth + 1)
		r.merge_sort(tipo, depth + 1)
		self.merge(l, r, tipo)

	def ordenar_titulo(self):
		cancion = self.proxima.elemento
		self.merge_sort('titulo')
		self.proxima = self.proxima.siguiente

	def ordenar_artista(self):
		cancion = self.proxima.elemento
		self.merge_sort('artista')
		self.proxima = self.proxima.siguiente
		
if __name__ == '__main__':
	rep = ListaReproduccion()
	with open("canciones/canciones.txt", 'r') as f:
		lineas = f.readlines()
		n = len(lineas) - 1
		for i in range(n):
			linea = lineas[i+1].split('\t')
			rep.agregar(Cancion(linea[1], linea[0], linea[2][0:len(linea[2]) - 1]))
	rep.ordenar_artista()
	print(rep)
