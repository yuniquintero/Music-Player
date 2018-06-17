from pathlib import Path
from PyQt5.QtCore import QFile

class Cancion():
	def __init__(self, titulo, artista, filepath):
		assert(len(titulo) > 0 and len(artista) > 0 and len(filepath) > 0)
		self.titulo = titulo
		self.artista = artista
		self.archivo = QFile(filepath)

	def __str__(self):
		string = "|{:^30s}|{:^30s}|".format(self.titulo, self.artista)
		return string

	def __repr__(self):
		return self.__str__()

	def es_igual(self, other):
		return self.titulo == other.titulo and self.artista == other.artista

	def es_menor_artista(self, other):
		if self.artista == other.artista:
			return self.titulo < other.titulo
		else:
			return self.artista < other.artista

	def es_menor_titulo(self, other):
		if self.titulo == other.titulo:
			return self.artista < other.artista
		else:
			return self.titulo < other.titulo