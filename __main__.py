import sys
from PyQt5.QtWidgets import QApplication
from src.vista.Interfaz_CuentasClaras import App_CuentasClaras
from src.logica.Logica import Logica

if __name__ == '__main__':
    #Punto inicial de la aplicación 

    logica = Logica()
    app = App_CuentasClaras(sys.argv, logica)
    sys.exit(app.exec_())