from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget

from functools import partial

class Vista_reporte_gastos_viajero(QWidget):
    #Ventana que muestra el reporte de gastos consolidados

    def __init__(self, interfaz):
        """
        Constructor de la ventana
        """
        super().__init__()

        # Se establecen las características de la ventana
        self.titulo = 'Cuentas Claras - Reporte de gastos por viajero'
        self.left = 80
        self.top = 80
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

        # Creación de la tabla en dónde se hará el reporte
        self.tabla_reporte = QScrollArea(self)
        self.tabla_reporte.setWidgetResizable(True)
        self.widget_tabla_reporte = QWidget()
        self.distribuidor_tabla_reporte = QGridLayout(self.widget_tabla_reporte)
        self.tabla_reporte.setWidget(self.widget_tabla_reporte)
        self.distribuidor_base.addWidget(self.tabla_reporte)

        self.distribuidor_tabla_reporte.setColumnStretch(0, 1)
        self.distribuidor_tabla_reporte.setColumnStretch(1, 1)
        self.distribuidor_tabla_reporte.setColumnStretch(2, 0)
        self.distribuidor_tabla_reporte.setColumnStretch(3, 0)

        # Creación de las etiquetas con los encabezados
        etiqueta_viajero = QLabel("Viajero")
        etiqueta_viajero.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_tabla_reporte.addWidget(etiqueta_viajero, 0, 0, Qt.AlignLeft)

        etiqueta_concepto = QLabel("Concepto")
        etiqueta_concepto.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_tabla_reporte.addWidget(etiqueta_concepto, 0, 1, Qt.AlignLeft)

        etiqueta_total = QLabel("Total")
        etiqueta_total.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_tabla_reporte.addWidget(etiqueta_total, 0, 2, 1, 2, Qt.AlignLeft)

        #Creación de los botones de funciones de la ventana
        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setFixedSize(200, 40)
        self.btn_volver.setToolTip("Añadir Actividad")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.btn_volver.setIconSize(QSize(120, 120))
        self.btn_volver.clicked.connect(self.volver)
        self.distribuidor_base.addWidget(self.btn_volver)
        self.distribuidor_base.setAlignment(self.btn_volver, Qt.AlignCenter)


    def mostar_reporte_gastos(self, lista_gastos):
        """
        Esta función puebla el reporte de gastos con la información en la lista
        """

        #Por cada iteración, llenamos con el nombre del viajero y sus gastos consolidados para la actividad
        numero_fila = 1
        for gasto in lista_gastos:

            etiqueta_viajero = QLabel(gasto["Nombre"] + ' ' + gasto["Apellido"])
            etiqueta_viajero.setWordWrap(True)
            self.distribuidor_tabla_reporte.addWidget(etiqueta_viajero, numero_fila, 0, Qt.AlignLeft)

            etiqueta_concepto = QLabel('Gastos consolidados')
            etiqueta_concepto.setWordWrap(True)
            self.distribuidor_tabla_reporte.addWidget(etiqueta_concepto, numero_fila, 1, Qt.AlignLeft)

            etiqueta_total = QLabel("${:,.2f}".format(gasto["Valor"]))
            etiqueta_total.setWordWrap(True)
            self.distribuidor_tabla_reporte.addWidget(etiqueta_total, numero_fila, 2, Qt.AlignLeft)

            numero_fila = numero_fila+1

        #Elemento para ajustar la forma de la tabla (y evitar que queden muy espaciados)
        self.distribuidor_tabla_reporte.layout().setRowStretch(numero_fila+1, 1)

    def volver(self):
        """
        Esta función permite volver a la ventana de la actividad
        """   
        self.hide()
        self.interfaz.mostrar_actividad()
