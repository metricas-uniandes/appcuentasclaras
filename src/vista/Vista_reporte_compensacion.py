from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from functools import partial
from PyQt5.QtWidgets import QWidget


class Vista_reporte_compensacion(QWidget):
    #Ventana que muestra el reporte de compensación

    def __init__(self, interfaz):
        """
        Constructor de la ventana
        """
        super().__init__()

        # Se establecen las características de la ventana
        self.titulo = 'Cuentas Claras - Reporte de compensación'
        self.width = 720
        self.height = 560

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.interfaz = interfaz
        self.inicializar_GUI()
        self.show()

    def inicializar_GUI(self):

        # inicializamos la ventana
        self.setWindowTitle(self.titulo)
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QIcon("src/recursos/smallLogo.png"))

        self.distribuidor_base = QVBoxLayout(self)

        self.tabla_compensacion = QScrollArea(self)
        self.tabla_compensacion.setWidgetResizable(True)
        self.widget_tabla_compensacion = QWidget()
        self.distribuidor_tabla_compensacion = QGridLayout(
            self.widget_tabla_compensacion)
        self.tabla_compensacion.setWidget(self.widget_tabla_compensacion)
        self.distribuidor_base.addWidget(self.tabla_compensacion)

        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setFixedSize(200, 40)
        self.btn_volver.setToolTip("Añadir Actividad")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.btn_volver.clicked.connect(self.volver)

        self.distribuidor_base.addWidget(self.btn_volver)
        self.distribuidor_base.setAlignment(self.btn_volver, Qt.AlignCenter)

    def mostrar_reporte_compensacion(self, matriz_compensacion):
        """
        Esta función construye el reporte de compensación a partir de una matriz
        """        

        self.matriz = matriz_compensacion

        for i in range(0, len(self.matriz)):
            for j in range(0, len(self.matriz)):
                
                if i == j:
                    #La etiqueta 0,0 debe estar vacía. Las etiquetas diagonales deben estar en negro
                    etiqueta_valor = QLabel("")
                    if i != 0:
                        etiqueta_valor = QLabel("")
                        etiqueta_valor.setStyleSheet(
                            "QLabel { background-color : #000; }")
                elif i == 0 or j == 0:
                    #Las etiquetas de la primera fila y la primera columna son nombres
                    etiqueta_valor = QLabel("{}".format(self.matriz[i][j]))
                    etiqueta_valor.setWordWrap(True)
                    etiqueta_valor.setFont(QFont("Times", weight=QFont.Bold))
                else:
                    #Las etiquetas restantes deben ser los montos de dinero
                    etiqueta_valor = QLabel(
                        "${:,.2f}".format(self.matriz[i][j]))
                    etiqueta_valor.setWordWrap(True)
                    etiqueta_valor.setToolTip(
                        self.matriz[0][i] + " debe " + "${:,.2f}".format(self.matriz[i][j]) + " a " + self.matriz[0][j])
                etiqueta_valor.setFixedSize(100, 40)
                self.distribuidor_tabla_compensacion.addWidget(
                    etiqueta_valor, i, j, Qt.AlignHCenter)

        #Elementos de espacio para ajustar las dimensiones de la tabla
        self.distribuidor_tabla_compensacion.layout().setRowStretch(len(self.matriz), 1)
        self.distribuidor_tabla_compensacion.layout().setColumnStretch(len(self.matriz), 1)


    def volver(self):
        """
        Esta función permite volver a la ventana de la actividad
        """   
        self.hide()
        self.interfaz.mostrar_actividad()
