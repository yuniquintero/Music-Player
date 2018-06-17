from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import *

from cancion import Cancion
from lista import ListaReproduccion

class Reproductor(QWidget):
    def __init__(self, parent = None):
    
        QWidget.__init__(self, parent)

        self.resize(200,50)

        self.buffer = QBuffer()
        self.data = QByteArray()
        self.__playlist = ListaReproduccion()
        
        format = QAudioFormat()
        format.setSampleSize(16)
        format.setSampleRate(44100) # 44100
        format.setChannelCount(1)
        format.setCodec("audio/x-wav")
        format.setByteOrder(QAudioFormat.LittleEndian)
        format.setSampleType(QAudioFormat.SignedInt)
        self.output = QAudioOutput(format, self)

        self.output.stateChanged.connect(self.foo)

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setPageStep(2)
        self.volumeSlider.setSliderPosition(50)

        self.playButton = QPushButton(self.tr("&Play"))
        self.stopButton = QPushButton(self.tr("&Stop"))
        self.pauseButton = QPushButton(self.tr("&Pause"))
        self.prevButton = QPushButton(self.tr("&Previous"))
        self.nextButton = QPushButton(self.tr("&Next"))

        self.volumeSlider.valueChanged.connect(self.changeVolume)
        self.playButton.clicked.connect(self.play)
        self.stopButton.clicked.connect(self.stop)
        self.pauseButton.clicked.connect(self.pause)
        self.nextButton.clicked.connect(self.next)
        self.prevButton.clicked.connect(self.prev)

        formLayout = QFormLayout()
        formLayout.addRow(self.tr("&Volume:"), self.volumeSlider)

        upperLayout = QHBoxLayout()
        upperLayout.addLayout(formLayout)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.pauseButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.stopButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.prevButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.nextButton)
        
        horizontalLayout = QVBoxLayout(self)
        horizontalLayout.addLayout(upperLayout)
        horizontalLayout.addStretch()
        horizontalLayout.addLayout(buttonLayout)
    
    def play(self):
        if self.output.state() == QAudio.ActiveState:
            return
        elif self.output.state() == QAudio.SuspendedState:
            self.output.resume()
            return

        if self.buffer.isOpen():
            self.buffer.close()

        if self.__playlist.proxima == None:
            return
        
        file = self.__playlist.proxima.elemento.archivo
        file.open(QIODevice.ReadOnly)
        
        self.data = file.readAll()
        file.close()

        self.buffer.setData(self.data)
        self.buffer.open(QIODevice.ReadOnly)
        self.buffer.seek(0)
        
        self.output.setVolume(0.5)
        
        self.__playlist.proxima = self.__playlist.proxima.siguiente

        self.output.start(self.buffer)

    def pause(self):
        if self.output.state() == QAudio.ActiveState:
            self.output.suspend()
        elif self.output.state() == QAudio.StoppedState:
            self.buffer.close()
            return
        elif self.output.state() == QAudio.SuspendedState:
            self.output.resume()

    def stop(self):
        if self.output.state() == QAudio.ActiveState:
            self.output.stop()

        if self.buffer.isOpen():
            self.buffer.close()

    def next(self):
        if self.__playlist.proxima == None:
            return

        self.output.stop()
        self.play()
    
    def prev(self):
        if self.__playlist.proxima == None:
            return

        self.__playlist.proxima = self.__playlist.proxima.anterior.anterior
        self.output.stop()
        self.play()

    def eliminar(self, title):
        self.__playlist.eliminar(title)

    def changeVolume(self, value):
        self.output.setVolume(value / 100)

    def foo(self,state):
        if state == QAudio.IdleState:
            self.next()

    def sonarDespues(self, s):
        self.__playlist.agregar(s)

    def sonarAntes(self, s):
        if self.__playlist != None:
            self.__playlist.proxima = self.__playlist.proxima.anterior

        self.__playlist.agregar_final(s)

        if self.__playlist != None:
            self.__playlist.proxima = self.__playlist.proxima.siguiente

    def mostrar(self):
        self.__playlist.mostrar()

    def size(self):
        return self.__playlist.numero_nodos

    def ordenar_por_titulo(self):
        self.__playlist.ordenar_titulo()

    def ordenar_por_artista(self):
        self.__playlist.ordenar_artista()
