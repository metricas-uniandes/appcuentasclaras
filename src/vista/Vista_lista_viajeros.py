from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *

from functools import partial
from .Vista_crear_viajero import Dialogo_crear_viajero

class Vista_lista_viajeros(QWidget):
    #Ventana que muestra la lista de viajeros

    def __init__(self, interfaz):
        """
        Constructor de la ventana
        """
        super().__init__()

        #Se establecen las características de la ventana
        self.titulo = 'CuentasClaras - Viajeros'
        self.interfaz=interfaz

        self.width = 400
        self.height = 330
        self.inicializar_GUI()
        self.show()


    def inicializar_GUI(self):

        # inicializamos la ventana
        self.setWindowTitle(self.titulo)
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
         
        self.distribuidor_base = QVBoxLayout(self)        

        #Creación de la tabla con la lista de viajeros
        self.tabla_viajeros = QScrollArea(self)
        self.tabla_viajeros.setWidgetResizable(True)
        self.tabla_viajeros.setFixedSize(375, 250)
        self.widget_tabla_viajeros = QWidget()
        self.distribuidor_tabla_viajeros = QGridLayout(self.widget_tabla_viajeros)
        self.tabla_viajeros.setWidget(self.widget_tabla_viajeros)
        self.distribuidor_base.addWidget(self.tabla_viajeros)

        #Creación del grupo de botones
        caja_botones = QGroupBox()
        caja_botones.setLayout(QHBoxLayout())

        #Creación de los botones
        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setFixedSize(150, 40)
        self.btn_volver.setToolTip("Volver")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.btn_volver.clicked.connect(self.volver)

        self.distribuidor_base.addStretch()
        self.btn_aniadir_viajero=QPushButton("Añadir Viajero",self)
        self.btn_aniadir_viajero.setFixedSize(150,40)
        self.btn_aniadir_viajero.setToolTip("Añadir Viajero")                
        self.btn_aniadir_viajero.setIcon(QIcon("src/recursos/006-add.png"))
        self.btn_aniadir_viajero.clicked.connect(self.mostrar_dialogo_insertar_viajero)

        #Se añaden los botones a la caja de botones
        caja_botones.layout().addWidget(self.btn_volver)
        caja_botones.layout().addWidget(self.btn_aniadir_viajero)
        caja_botones.layout().setContentsMargins(0, 0, 0, 0)
        caja_botones.setObjectName("MyBox")
        caja_botones.setStyleSheet("#MyBox{border:3px}")
        self.distribuidor_base.addWidget(caja_botones)

        self.distribuidor_tabla_viajeros.setColumnStretch(0, 0)
        self.distribuidor_tabla_viajeros.setColumnStretch(1, 0)
        self.distribuidor_tabla_viajeros.setColumnStretch(2, 0)

        self.distribuidor_tabla_viajeros.setSpacing(0)

        #Creación de las etiquetas de encabezado
        etiqueta_nombre = QLabel("Nombre")
        etiqueta_nombre.setFixedSize(145,40)
        etiqueta_nombre.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_tabla_viajeros.addWidget(etiqueta_nombre, 0, 0, Qt.AlignTop)

        etiqueta_apellido = QLabel("Apellido")
        etiqueta_apellido.setFixedSize(145,40)
        etiqueta_apellido.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_tabla_viajeros.addWidget(etiqueta_apellido, 0, 1, Qt.AlignTop)

        etiqueta_accion = QLabel("Accion")
        etiqueta_accion.setFixedSize(60,40)
        etiqueta_accion.setFont(QFont("Times",weight=QFont.Bold)) 
        etiqueta_accion.setAlignment(Qt.AlignCenter)
        self.distribuidor_tabla_viajeros.addWidget(etiqueta_accion, 0, 2, 1, 2, Qt.AlignTop)
        
    def mostrar_viajeros(self, viajeros):
        """
        Esta función muestra la lista de viajeros
        """
        self.viajeros = viajeros
        
        #Este pedazo de código borra todos los contenidos anteriores de la tabla (salvo los encabezados)
        while self.distribuidor_tabla_viajeros.count()>3:
            child = self.distribuidor_tabla_viajeros.takeAt(3)
            if child.widget():
                child.widget().deleteLater()

        #Ciclo para poblar la tabla
        numero_fila = 0
        for viajero in self.viajeros:

            etiqueta_nombre=QLabel(viajero["Nombre"])          
            etiqueta_nombre.setWordWrap(True)
            etiqueta_nombre.setFixedSize(90,40)
            self.distribuidor_tabla_viajeros.addWidget(etiqueta_nombre, numero_fila+1,0, Qt.AlignTop)

            etiqueta_apellido=QLabel(viajero["Apellido"])          
            etiqueta_apellido.setWordWrap(True)
            etiqueta_apellido.setFixedSize(90,40)
            self.distribuidor_tabla_viajeros.addWidget(etiqueta_apellido, numero_fila+1,1, Qt.AlignTop)

            etiqueta_eliminar=QPushButton("",self)
            etiqueta_eliminar.setToolTip("Delete")
            etiqueta_eliminar.setFixedSize(30,30)
            etiqueta_eliminar.setIcon(QIcon("src/recursos/005-delete.png"))
            etiqueta_eliminar.clicked.connect(partial(self.eliminar_viajero, numero_fila) )
            self.distribuidor_tabla_viajeros.addWidget(etiqueta_eliminar, numero_fila+1,2,Qt.AlignTop)

            boton_editar=QPushButton("",self)
            boton_editar.setToolTip("Edit")
            boton_editar.setFixedSize(30,30)
            boton_editar.setIcon(QIcon("src/recursos/004-edit-button.png"))
            boton_editar.clicked.connect(partial(self.mostrar_dialogo_editar_viajero, numero_fila) )
            self.distribuidor_tabla_viajeros.addWidget(boton_editar, numero_fila+1,3,Qt.AlignTop)

            numero_fila=numero_fila+1

        #Elemento para ajustar la forma de la tabla (y evitar que queden muy espaciados)
        self.distribuidor_tabla_viajeros.layout().setRowStretch(numero_fila+1, 1)

    def mostrar_dialogo_editar_viajero(self, indice_viajero):
        """
        Esta función ejecuta el diálogo para editar un viajero
        """    
        dialogo=Dialogo_crear_viajero(self.viajeros[indice_viajero])        
        dialogo.exec_()
        if dialogo.resultado==1:            
            self.interfaz.editar_viajero(indice_viajero, dialogo.texto_nombre.text(), dialogo.texto_apellido.text())

    def eliminar_viajero(self, indice_viajero):
        """
        Esta función informa a la interfaz del viajero a eliminar
        """    
        self.interfaz.eliminar_viajero(indice_viajero)          


    def mostrar_dialogo_insertar_viajero(self):
        """
        Esta función ejecuta el diálogo para crear un nuevo viajero
        """    
        dialogo=Dialogo_crear_viajero(None)        
        dialogo.exec_()
        if dialogo.resultado==1:            
            self.interfaz.insertar_viajero(dialogo.texto_nombre.text(), dialogo.texto_apellido.text())
        
    def volver(self):
        """
        Esta función permite volver a la ventana de lista de actividades
        """    
        self.interfaz.mostrar_vista_lista_actividades()
        self.close()

   