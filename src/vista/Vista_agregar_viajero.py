from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Dialogo_agregar_viajeros(QDialog):
    #Diálogo para agregar viajeros a una actividad  

    def __init__(self):
        """
        Constructor del diálogo
        """    
        super().__init__()

        self.setFixedSize(340, 250)
        self.setWindowIcon(
            QIcon("src/devcuentasclaras/recursos/smallLogo.png"))
        self.setWindowTitle("Añadir viajeros a actividad")
        self.resultado = ""

        self.widget_dialogo = QListWidget()

        self.distribuidor_dialogo = QGridLayout()
        self.setLayout(self.distribuidor_dialogo)
        numero_fila = 0

        #Creación de las etiquetas
        etiqueta_descripcion = QLabel("Viajeros disponibles")
        etiqueta_descripcion.setFont(QFont("Times", weight=QFont.Bold))
        self.distribuidor_dialogo.addWidget(
            etiqueta_descripcion, numero_fila, 0, 1, 3)
        numero_fila = numero_fila+1

        #Creación de la tabla que contiene todos los viajeros disponibles

        self.tabla_viajeros = QScrollArea()
        self.tabla_viajeros.setWidgetResizable(True)
        widget_tabla_viajeros = QWidget()
        self.distribuidor_tabla_viajeros = QGridLayout(widget_tabla_viajeros)
        self.tabla_viajeros.setWidget(widget_tabla_viajeros)
        self.distribuidor_dialogo.addWidget(
            self.tabla_viajeros, numero_fila, 0, 1, 3)

        numero_fila+=1

        #Creación de los botones para guardar y cancelar

        self.btn_guardar = QPushButton("Guardar")
        self.distribuidor_dialogo.addWidget(self.btn_guardar, numero_fila, 1)
        self.btn_guardar.clicked.connect(self.guardar)

        self.btn_cancelar = QPushButton("Cancelar")
        self.distribuidor_dialogo.addWidget(self.btn_cancelar, numero_fila, 2)
        self.btn_cancelar.clicked.connect(self.cancelar)



    def mostrar_viajeros(self, viajeros):
        """
        Esta función muestra los viajeros en la tabla
        """    
        self.viajeros = viajeros
        self.lista_cajas_de_chequeo = []
        indice_viajero = 0
        numero_fila = 4
        for viajero in self.viajeros:
            caja_de_chequeo = QCheckBox(viajero["Nombre"])
            self.lista_cajas_de_chequeo.append(caja_de_chequeo)

            if viajero["Presente"]:
                caja_de_chequeo.setChecked(True)

            self.distribuidor_tabla_viajeros.addWidget(
                self.lista_cajas_de_chequeo[indice_viajero], indice_viajero, 0)
            indice_viajero = indice_viajero+1

    def guardar(self):
        """
        Esta función envía la información de que se han guardado los cambios
        """   
        idx = 0
        for idx in range(len(self.lista_cajas_de_chequeo)):
            checkbox = self.lista_cajas_de_chequeo[idx]
            if checkbox.isChecked():
                self.viajeros[idx]["Presente"] = True
            else:
                self.viajeros[idx]["Presente"] = False

        self.resultado = 1
        self.close()
        return self.resultado

    def cancelar(self):
        """
        Esta función envía la información de que se ha cancelado la operación
        """ 
        self.resultado = 0
        self.close()
        return self.resultado
