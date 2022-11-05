from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from functools import partial

from .Vista_crear_actividad import Dialogo_crear_actividad
from .Vista_agregar_viajero import Dialogo_agregar_viajeros


class Vista_lista_actividades(QWidget):
    #Ventana que muestra la lista de actividades

    def __init__(self, interfaz):
        """
        Constructor de la ventanas
        """
        super().__init__()
        
        self.interfaz=interfaz
       
        #Se establecen las características de la ventana
        self.title = 'Cuentas Claras'
        self.width = 720
        self.height = 700      
        self.inicializar_GUI()

    def inicializar_GUI(self):
        
        #inicializamos la ventana
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
         
        self.distribuidor_base = QVBoxLayout(self)

        #Creación del logo de encabezado
        self.logo=QLabel(self)
        self.pixmap = QPixmap("src/recursos/CuentasClarasHeader.png")        
        self.logo.setPixmap(self.pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        self.distribuidor_base.addWidget(self.logo,alignment=Qt.AlignCenter)

        #Creación de las etiquetsa con textos de bienvenida
        self.etiqueta_bienvenida=QLabel("!!Bienvenido a CuentasClaras!!")                               
        self.etiqueta_bienvenida.setAlignment(Qt.AlignCenter)
        self.distribuidor_base.addWidget(self.etiqueta_bienvenida,Qt.AlignCenter)
        
        self.etiqueta_descripcion=QLabel("La unica aplicacion que te permite organizar actividades con tus amigos de forma justa")                               
        self.etiqueta_descripcion.setAlignment(Qt.AlignCenter)
        self.distribuidor_base.addWidget(self.etiqueta_descripcion,Qt.AlignCenter)

        #Creación del espacio de los botones
        self.widget_botones=QWidget()
        self.distribuidor_botones=QGridLayout()
        self.widget_botones.setLayout(self.distribuidor_botones)

        #Creación de los botones
        self.btn_aniadir_actividad=QPushButton("Añadir Actividad",self)
        self.btn_aniadir_actividad.setFixedSize(200,40)
        self.btn_aniadir_actividad.setToolTip("Añadir Actividad")                
        self.btn_aniadir_actividad.setIcon(QIcon("src/recursos/006-add.png"))
        self.btn_aniadir_actividad.setIconSize(QSize(120,120))
        self.distribuidor_botones.addWidget(self.btn_aniadir_actividad,0,0,Qt.AlignLeft)
        self.btn_aniadir_actividad.clicked.connect(self.mostrar_dialogo_insertar_actividad)

        self.btn_ver_viajeros=QPushButton("Ver Viajeros",self)
        self.btn_ver_viajeros.setFixedSize(200,40)
        self.btn_ver_viajeros.setToolTip("Ver Viajeros")                
        self.btn_ver_viajeros.setIcon(QIcon("src/recursos/010-people-24.png"))
        self.btn_ver_viajeros.setIconSize(QSize(120,120))                
        self.btn_ver_viajeros.clicked.connect(self.mostrar_viajeros)
        self.distribuidor_botones.addWidget(self.btn_ver_viajeros,0,1,Qt.AlignRight)        
        self.distribuidor_base.addWidget(self.widget_botones,Qt.AlignCenter)

        #Creación del área con la información de las actividades
        self.tabla_actividades = QScrollArea(self)
        self.tabla_actividades.setWidgetResizable(True)
        self.tabla_actividades.setFixedSize(700, 450)
        self.widget_tabla_actividades = QWidget()
        self.distribuidor_tabla_actividades = QGridLayout()        
        self.widget_tabla_actividades.setLayout(self.distribuidor_tabla_actividades);                
        self.tabla_actividades.setWidget(self.widget_tabla_actividades)
        self.distribuidor_base.addWidget(self.tabla_actividades)

        #Hacemos la ventana visible
        self.show()


    def mostrar_actividades(self, lista_actividades):
        """
        Esta función puebla la tabla con las activiades
        """
        self.actividades = lista_actividades

        #Este pedazo de código borra todo lo que no sean encabezados, es decir, a partir del tercer elemento.
        while self.distribuidor_tabla_actividades.count()>2:
            child = self.distribuidor_tabla_actividades.takeAt(2)
            if child.widget():
                child.widget().deleteLater()

        self.distribuidor_tabla_actividades.setColumnStretch(0,1)
        self.distribuidor_tabla_actividades.setColumnStretch(1,0)
        self.distribuidor_tabla_actividades.setColumnStretch(2,0)
        self.distribuidor_tabla_actividades.setColumnStretch(3,0)
        self.distribuidor_tabla_actividades.setColumnStretch(4,0)
        self.distribuidor_tabla_actividades.setColumnStretch(4,0)
        numero_fila=0

        #Ciclo para llenar la tabla
        if (self.actividades!= None and len(self.actividades)>0) :
            self.tabla_actividades.setVisible(True)

            #Creación de las etiquetas

            etiqueta_actividad=QLabel("Actividad")                      
            etiqueta_actividad.setMinimumSize(QSize(0,0))
            etiqueta_actividad.setMaximumSize(QSize(65525,65525))
            etiqueta_actividad.setAlignment(Qt.AlignCenter)
            etiqueta_actividad.setFont(QFont("Times",weight=QFont.Bold)) 
            self.distribuidor_tabla_actividades.addWidget(etiqueta_actividad, 0,0, Qt.AlignCenter)

            etiqueta_acciones=QLabel("Acciones")                      
            etiqueta_acciones.setMinimumSize(QSize(0,0))
            etiqueta_acciones.setMaximumSize(QSize(65525,65525))
            etiqueta_acciones.setAlignment(Qt.AlignCenter)
            etiqueta_acciones.setFont(QFont("Times",weight=QFont.Bold))               
            self.distribuidor_tabla_actividades.addWidget(etiqueta_acciones, 0,1,1,5, Qt.AlignCenter)
            
            for item in self.actividades:
                numero_fila=numero_fila+1

                etiqueta_actividad=QLabel(item)          
                etiqueta_actividad.setWordWrap(True)
                self.distribuidor_tabla_actividades.addWidget(etiqueta_actividad,numero_fila,0)

                #Creación de los botones asociados a cada acción

                btn_terminar=QPushButton("",self)
                btn_terminar.setToolTip("Terminar")
                btn_terminar.setFixedSize(40,40)
                btn_terminar.setIcon(QIcon("src/recursos/001-no-stopping.png"))
                btn_terminar.clicked.connect(partial(self.terminar_actividad,numero_fila-1) )
                self.distribuidor_tabla_actividades.addWidget(btn_terminar,numero_fila,1,Qt.AlignCenter)

                btn_ver_actividad=QPushButton("",self)
                btn_ver_actividad.setToolTip("Ver")
                btn_ver_actividad.setFixedSize(40,40)
                btn_ver_actividad.setIcon(QIcon("src/recursos/002-eye-variant-with-enlarged-pupil.png"))
                btn_ver_actividad.clicked.connect(partial(self.mostrar_actividad,numero_fila-1) )
                self.distribuidor_tabla_actividades.addWidget(btn_ver_actividad,numero_fila,2,Qt.AlignCenter)

                btn_ver_viajeros=QPushButton("",self)
                btn_ver_viajeros.setToolTip("Viajeros")
                btn_ver_viajeros.setFixedSize(40,40)
                btn_ver_viajeros.setIcon(QIcon("src/recursos/003-multiple-users-silhouette.png"))
                btn_ver_viajeros.clicked.connect(partial(self.mostrar_dialogo_insertar_viajeros,item) )
                self.distribuidor_tabla_actividades.addWidget(btn_ver_viajeros,numero_fila,3,Qt.AlignCenter)

                btn_editar=QPushButton("",self)
                btn_editar.setToolTip("Edit")
                btn_editar.setFixedSize(40,40)
                btn_editar.setIcon(QIcon("src/recursos/004-edit-button.png"))
                btn_editar.clicked.connect(partial(self.mostrar_dialogo_editar_actividad,numero_fila -1 ) )
                self.distribuidor_tabla_actividades.addWidget(btn_editar,numero_fila,4,Qt.AlignCenter)


                btn_eliminar=QPushButton("",self)
                btn_eliminar.setToolTip("Delete")
                btn_eliminar.setFixedSize(40,40)
                btn_eliminar.setIcon(QIcon("src/recursos/005-delete.png"))
                btn_eliminar.clicked.connect(partial(self.eliminar_actividad,numero_fila -1) )
                self.distribuidor_tabla_actividades.addWidget(btn_eliminar,numero_fila,5,Qt.AlignCenter)
        else:
                self.tabla_actividades.setVisible(False)

        #Elemento para ajustar la forma de la tabla (y evitar que queden muy espaciados)
        self.distribuidor_tabla_actividades.layout().setRowStretch(numero_fila+2, 1)

    def terminar_actividad(self, actividad):
        """
        Esta función informa a la interfaz para terminar una actividad
        """
        self.interfaz.terminar_actividad(actividad)

    def mostrar_actividad(self,actividad): 
        """
        Esta función informa a la interfaz para desplegar la ventana de la actividad
        """        
        self.hide()
        self.interfaz.mostrar_actividad(actividad)
 
    def mostrar_viajeros(self):
        """
        Esta función informa a la interfaz para desplegar la ventana de la lista de viajeros
        """
        self.hide()
        self.interfaz.mostrar_viajeros()
        
    def mostrar_dialogo_insertar_actividad(self):
        """
        Esta función ejecuta el diálogo para insertar una actividad
        """
        dialogo = Dialogo_crear_actividad(None)        
        dialogo.exec_()
        if dialogo.resultado == 1:
            self.interfaz.insertar_actividad(dialogo.texto_nombre.text())

    def mostrar_dialogo_editar_actividad(self,indice_actividad):
        """
        Esta función ejecuta el diálogo para editar una actividad
        """
        dialogo = Dialogo_crear_actividad(self.actividades[indice_actividad])        
        dialogo.exec_()
        if dialogo.resultado == 1:
            self.interfaz.editar_actividad(indice_actividad, dialogo.texto_nombre.text())
            
    def mostrar_dialogo_insertar_viajeros(self,actividad):   
        """
        Esta función ejecuta el diálogo para agregar un viajero
        """     
        dialogo=Dialogo_agregar_viajeros()
        dialogo.mostrar_viajeros(self.interfaz.dar_viajeros_en_actividad(actividad))
        dialogo.exec_()
        if dialogo.resultado == 1:
            self.interfaz.actualizar_viajeros(actividad ,dialogo.viajeros)

    def eliminar_actividad(self,indice_actividad): 
        """
        Esta función elimina una actividad tras solicitar una confirmación
        """
        mensaje_confirmacion=QMessageBox()
        mensaje_confirmacion.setIcon(QMessageBox.Question)
        mensaje_confirmacion.setText("¿Esta seguro de que desea borrar esta actividad?\nRecuerde que esta acción es irreversible")        
        mensaje_confirmacion.setWindowTitle("¿Desea borrar esta actividad?")
        mensaje_confirmacion.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
        mensaje_confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No ) 
        respuesta=mensaje_confirmacion.exec_()
        if respuesta == QMessageBox.Yes:
             self.interfaz.eliminar_actividad(indice_actividad)
    


        
