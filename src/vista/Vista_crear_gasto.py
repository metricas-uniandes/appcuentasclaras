from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from functools import partial


class Dialogo_crear_gasto(QDialog):
    #Diálogo para crear o editar un gasto

    def __init__(self,viajeros, gasto):
        """
        Constructor del diálogo
        """   
        super().__init__()

        
        self.setFixedSize(340, 250)
        self.setWindowIcon(QIcon("src/devcuentasclaras/recursos/smallLogo.png"))

        self.resultado = ""
        self.viajeros = viajeros

        self.widget_lista = QListWidget()
        

        distribuidor_dialogo = QGridLayout()
        self.setLayout(distribuidor_dialogo)
        numero_fila=0
        
        #Si el diálogo se usa para crear o editar, el título cambia.

        titulo=""
        if(gasto==None):
            titulo="Nuevo Gasto"
        else:
            titulo="Editar Gasto"
      

        self.setWindowTitle(titulo)

        #Creación de las etiquetas y campos de texto

        etiqueta_concepto=QLabel("Concepto")
        distribuidor_dialogo.addWidget(etiqueta_concepto,numero_fila,0,1,3)                
        numero_fila=numero_fila+1

        self.texto_concepto=QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_concepto,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        etiqueta_fecha=QLabel("Fecha")
        distribuidor_dialogo.addWidget(etiqueta_fecha,numero_fila,0,1,3)                
        numero_fila=numero_fila+1

        #Campo fecha es un elemento especial para modificar fechas
        self.campo_fecha=QDateEdit(self)
        distribuidor_dialogo.addWidget(self.campo_fecha,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        etiqueta_valor=QLabel("Valor")
        distribuidor_dialogo.addWidget(etiqueta_valor,numero_fila,0,1,3)                
        numero_fila=numero_fila+1

        self.texto_valor=QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_valor,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        etiqueta_viajero=QLabel("Viajero")
        distribuidor_dialogo.addWidget(etiqueta_viajero,numero_fila,0,1,3)                
        numero_fila=numero_fila+1

        
        self.lista_viajeros = QComboBox(self)

        for viajero in viajeros:
            self.lista_viajeros.addItem(viajero["Nombre"] + " " +viajero["Apellido"])
        
             
        distribuidor_dialogo.addWidget(self.lista_viajeros,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        #Creación de los botones para guardar o cancelar

        self.btn_guardar = QPushButton("Guardar")
        distribuidor_dialogo.addWidget(self.btn_guardar ,numero_fila,1)
        self.btn_guardar.clicked.connect(self.guardar)

        self.btn_cancelar = QPushButton("Cancelar")
        distribuidor_dialogo.addWidget(self.btn_cancelar ,numero_fila,2)
        self.btn_cancelar.clicked.connect(self.cancelar)

        #Si el diálogo se usa para editar, se debe poblar con la información del gasto a editar
        if gasto != None:
            self.texto_concepto.setText(gasto["Concepto"])
            self.campo_fecha.setDate(QDate.fromString(gasto["Fecha"],"dd-MM-yyyy"))
            self.texto_valor.setText(str(gasto["Valor"]))
            indice = self.lista_viajeros.findText(gasto["Nombre"]+" "+gasto["Apellido"])
            self.lista_viajeros.setCurrentIndex(indice)

    
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

