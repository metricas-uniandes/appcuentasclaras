from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from functools import partial


class Dialogo_crear_viajero(QDialog):
    #Diálogo para crear o editar un viajero

    def __init__(self,viajero):
        """
        Constructor del diálogo
        """   
        super().__init__()

        
        self.setFixedSize(400, 200)
        self.setWindowIcon(QIcon("src/devcuentasclaras/recursos/smallLogo.png"))

        self.resultado = ""

        self.widget_dialogo = QListWidget()
        
        distribuidor_dialogo = QGridLayout()
        self.setLayout(distribuidor_dialogo)
        numero_fila=0
        
        #Si se va a crear un nuevo viajero o se va a editar, usamos el mismo diálogo
        titulo=""
        if(viajero==None):
            titulo="Nuevo Viajero"
        else:
            titulo="Editar Viajero"

        self.setWindowTitle("CuentasClaras - {}".format(titulo))
       
        #Creación de las etiquetas y los campos de texto

        etiqueta_nombre=QLabel("Nombre")
        distribuidor_dialogo.addWidget(etiqueta_nombre,numero_fila,0,1,3)                
        numero_fila=numero_fila+1

        self.texto_nombre=QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_nombre,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        etiqueta_apellido=QLabel("Apellido")
        distribuidor_dialogo.addWidget(etiqueta_apellido,numero_fila,0,1,3)                
        numero_fila=numero_fila+1
        
        self.texto_apellido=QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_apellido,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        #Creación de los botones para guardar o cancelar

        self.btn_guardar = QPushButton("Guardar")
        distribuidor_dialogo.addWidget(self.btn_guardar ,numero_fila,1)
        self.btn_guardar.clicked.connect(self.guardar)

        self.btn_cancelar = QPushButton("Cancelar")
        distribuidor_dialogo.addWidget(self.btn_cancelar ,numero_fila,2)
        self.btn_cancelar.clicked.connect(self.cancelar)

        #Si el diálogo se va a usar para editar, se pone la información correspondiente en los campos de texto

        if (viajero!=None):
            self.texto_nombre.setText(viajero["Nombre"])
            self.texto_apellido.setText(viajero["Apellido"])


    def guardar(self):
        """
        Esta función envía la información de que se han guardado los cambios
        """   
        self.resultado=1
        self.close()
        return self.resultado


    def cancelar(self):
        """
        Esta función envía la información de que se ha cancelado la operación
        """   
        self.resultado=0
        self.close()
        return self.resultado


