from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from functools import partial
from .Vista_crear_gasto import Dialogo_crear_gasto


class Vista_actividad(QWidget):
    #Ventana de la actividad
    def __init__(self,principal):
        """
        Constructor de la ventana
        """   
        super().__init__()

        self.titulo = 'Cuentas Claras - Detalle de'
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.interfaz=principal            

        self.width = 720
        self.height = 550
        self.inicializar_GUI()
        self.show()
       

    def inicializar_GUI(self):

        # inicializamos la ventana
        self.setWindowTitle(self.titulo)
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QIcon("src/recursos/smallLogo.png"))

        self.distribuidor_base = QVBoxLayout(self)
 
        #Creación de la caja con los botones

        self.widget_botones = QWidget()
        self.distribuidor_botones = QGridLayout()
        self.widget_botones.setLayout(self.distribuidor_botones)
        self.distribuidor_base.addWidget(self.widget_botones, Qt.AlignTop)

        #Creación de los botones con las diferentes operaciones
        self.btn_aniadir_gasto = QPushButton("Añadir Gasto", self)
        self.btn_aniadir_gasto.setFixedSize(200, 40)
        self.btn_aniadir_gasto.setToolTip("Añadir Gasto")
        self.btn_aniadir_gasto.setIcon(QIcon("src/recursos/006-add.png"))
        self.distribuidor_botones.addWidget(self.btn_aniadir_gasto, 0, 0, Qt.AlignCenter)
        self.btn_aniadir_gasto.clicked.connect(self.crear_gasto)

        self.btn_reporte_gastos_viajeros = QPushButton("Gastos por Viajero", self)
        self.btn_reporte_gastos_viajeros.setFixedSize(200, 40)
        self.btn_reporte_gastos_viajeros.setToolTip("Gastos por Viajero")
        self.btn_reporte_gastos_viajeros.setIcon(QIcon("src/recursos/008-data-spreadsheet.png"))
        self.distribuidor_botones.addWidget(self.btn_reporte_gastos_viajeros, 0, 1, Qt.AlignCenter)
        self.btn_reporte_gastos_viajeros.clicked.connect(self.mostrar_reporte_gastos_por_viajero)

        self.btn_reporte_compensacion = QPushButton("Compensación", self)
        self.btn_reporte_compensacion.setFixedSize(200, 40)
        self.btn_reporte_compensacion.setToolTip("Compensación")
        self.btn_reporte_compensacion.setIcon(QIcon("src/recursos/009-money.png"))
        self.distribuidor_botones.addWidget(self.btn_reporte_compensacion, 0, 2, Qt.AlignCenter)
        self.btn_reporte_compensacion.clicked.connect(self.mostrar_reporte_comensacion)
        
        #Creación de la tabla en donde se mostrarán los gastos 
        self.tabla_actividades = QScrollArea(self)
        self.tabla_actividades.setFixedSize(700, 400)
        self.tabla_actividades.setWidgetResizable(True)
        self.widget_contenidos_tabla_actividades = QWidget()
        self.distribuidor_actividades = QGridLayout(self.widget_contenidos_tabla_actividades)
        self.tabla_actividades.setWidget(self.widget_contenidos_tabla_actividades)
        self.distribuidor_base.addWidget(self.tabla_actividades, Qt.AlignTop)

        #Creación del botón final para regresar atrás
        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setFixedSize(200, 40)
        self.btn_volver.setToolTip("Añadir Actividad")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.btn_volver.clicked.connect(self.volver)
        self.distribuidor_base.addWidget(self.btn_volver)
        self.distribuidor_base.setAlignment(self.btn_volver, Qt.AlignCenter)

        etiqueta_nombre = QLabel("Viajero")
        etiqueta_nombre.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_actividades.addWidget(etiqueta_nombre, 0, 0, Qt.AlignLeft)

        etiqueta_fecha = QLabel("Fecha")
        etiqueta_fecha.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_actividades.addWidget(etiqueta_fecha, 0, 1, Qt.AlignLeft)

        etiqueta_concepto = QLabel("Concepto")
        etiqueta_concepto.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_actividades.addWidget(etiqueta_concepto, 0, 2, Qt.AlignLeft)

        etiqueta_valor = QLabel("Valor")
        etiqueta_valor.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_actividades.addWidget(etiqueta_valor, 0, 3, Qt.AlignLeft)

        etiqueta_accion = QLabel("Accion")
        etiqueta_accion.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_actividades.addWidget(etiqueta_accion, 0, 4, 1, 2, Qt.AlignCenter)

    def mostrar_gastos_por_actividad(self, actividad, gastos):
        """
        Esta función puebla la tabla de gastos para la actividad
        """   
        self.titulo+=" "+actividad
        self.setWindowTitle(self.titulo)

        self.gastos = gastos

        #Este pedazo de código borra todos los contenidos anteriores de la tabla (salvo los encabezados)
        while self.distribuidor_actividades.count()>5:
            child = self.distribuidor_actividades.takeAt(5)
            if child.widget():
                child.widget().deleteLater()

        self.distribuidor_actividades.setColumnStretch(0, 1)
        self.distribuidor_actividades.setColumnStretch(1, 1)
        self.distribuidor_actividades.setColumnStretch(2, 1)
        self.distribuidor_actividades.setColumnStretch(3, 1)
        self.distribuidor_actividades.setColumnStretch(4, 0)
        self.distribuidor_actividades.setColumnStretch(5, 0)

        if (len(gastos)<1):
            self.btn_reporte_gastos_viajeros.setEnabled(False)
            self.btn_reporte_compensacion.setEnabled(False)

        numero_fila=1
        
        #Ciclo para llenar los gastos
        for gasto in self.gastos:

            etiqueta_nombre = QLabel(gasto["Nombre"] + " " + gasto["Apellido"] )
            etiqueta_nombre.setWordWrap(True)
            self.distribuidor_actividades.addWidget(etiqueta_nombre, numero_fila, 0)

            etiqueta_fecha = QLabel(gasto["Fecha"])
            etiqueta_fecha.setWordWrap(True)
            self.distribuidor_actividades.addWidget(etiqueta_fecha, numero_fila, 1)

            etiqueta_concepto = QLabel(gasto["Concepto"])
            etiqueta_concepto.setWordWrap(True)
            self.distribuidor_actividades.addWidget(etiqueta_concepto, numero_fila, 2)

            etiqueta_valor = QLabel("${:,.2f}".format(gasto["Valor"]))
            etiqueta_valor.setWordWrap(True)
            self.distribuidor_actividades.addWidget(etiqueta_valor, numero_fila, 3, Qt.AlignLeft)

            btn_editar = QPushButton("", self)
            btn_editar.setToolTip("Edit")
            btn_editar.setGeometry(0, 0, 40, 40)
            btn_editar.setFixedSize(40, 40)
            btn_editar.setIcon(QIcon("src/recursos/004-edit-button.png"))
            btn_editar.setIconSize(QSize(40, 40))
            btn_editar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn_editar.clicked.connect(partial(self.editar_gasto, numero_fila-1))
            self.distribuidor_actividades.addWidget(btn_editar, numero_fila, 4, Qt.AlignCenter)

            btn_eliminar = QPushButton("", self)
            btn_eliminar.setToolTip("Delete")
            btn_eliminar.setGeometry(0, 0, 40, 40)
            btn_eliminar.setFixedSize(40, 40)
            btn_eliminar.setIcon(QIcon("src/recursos/005-delete.png"))
            btn_eliminar.setIconSize(QSize(40, 40))
            btn_eliminar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn_eliminar.clicked.connect(partial(self.eliminar_gasto, numero_fila-1))
            self.distribuidor_actividades.addWidget(btn_eliminar, numero_fila, 5, Qt.AlignCenter)

            numero_fila=numero_fila+1
        
        #Elemento para ajustar la forma de la tabla (y evitar que queden muy espaciados)
        elemento_de_espacio = QSpacerItem(140, 360-numero_fila*40 if numero_fila*40<=360 else 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.distribuidor_actividades.addItem(elemento_de_espacio, numero_fila, 0, 1, 3)


    def eliminar_gasto(self, indice_gasto):
        """
        Esta función informa a la interfaz del gasto a eliminar
        """    
        self.interfaz.eliminar_gasto(indice_gasto)

    def volver(self):
        """
        Esta función permite volver a la lista de actividades
        """    
        self.hide()
        self.interfaz.mostrar_vista_lista_actividades()

    def mostrar_reporte_comensacion(self):
        """
        Esta función informa a la interfaz para mostrar la ventana del reporte de compensación
        """    
        self.hide()
        self.interfaz.mostrar_reporte_compensacion()
        
    def mostrar_reporte_gastos_por_viajero(self):
        """
        Esta función informa a la interfaz para mostrar la ventana de los gastos consolidados
        """    
        self.hide()
        self.interfaz.mostrar_reporte_gastos_viajero()
    
    def crear_gasto(self):
        """
        Esta función ejecuta el diálogo para crear un gasto
        """    
        dialogo = Dialogo_crear_gasto(self.interfaz.dar_viajeros(), None)
        dialogo.exec_()
        if dialogo.resultado == 1:
            self.interfaz.insertar_gasto(dialogo.texto_concepto.text(), str(dialogo.campo_fecha.date().toPyDate().strftime("%d-%m-%Y")), dialogo.texto_valor.text(), dialogo.lista_viajeros.currentText().split(" ")[0], dialogo.lista_viajeros.currentText().split(" ")[-1])
            

    def editar_gasto(self, indice_gasto):
        """
        Esta función ejecuta el diálogo para editar un gasto
        """    
        dialogo = Dialogo_crear_gasto(self.interfaz.dar_viajeros(), self.gastos[indice_gasto])
        dialogo.exec_()
        if dialogo.resultado == 1:
            self.interfaz.editar_gasto(indice_gasto , dialogo.texto_concepto.text(), str(dialogo.campo_fecha.date().toPyDate().strftime("%d-%m-%Y")), dialogo.texto_valor.text(), dialogo.lista_viajeros.currentText().split(" ")[0], dialogo.lista_viajeros.currentText().split(" ")[-1])

