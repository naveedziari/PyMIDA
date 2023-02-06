import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from PyQt5.uic import *
#from PyQt5 import QtCore, QtWidgets


class MainWindow(QWidget):

	def __init__(self,parent = None):

		QMainWindow.__init__(self,parent)
		
		self.height = 500
		self.width = 500
		self.init_ui()
		#self.label.show()
		self.setWindowTitle('Manual MIDA')


	def init_ui(self):
		molecular_formula = QLabel(self)
		molecular_formula.setStyleSheet('QLabel {color: #FFFF00;}')
		molecular_formula.setText('Formula: ')
		molecular_formula.setFont(QFont('Helvetica', 48)) 
		molecular_formula.setAlignment(QtCore.Qt.AlignLeft)
		molecular_formula.show()


if __name__ == "__main__":
	app = QApplication(sys.argv[1:])

	app.setStyle("Fusion")
	palette = QPalette()



	palette.setColor(QPalette.Window, QColor(8, 8, 100))
	palette.setColor(QPalette.WindowText, Qt.white)
	app.setPalette(palette)


	window = MainWindow()
	window.show()
	sys.exit(app.exec_())


# app = QtWidgets.QApplication([sys.argv [1:]])
# frm = QtWidgets.QFrame()
# win = QMainWindow()
# win.setCentralWidget(frm)
# win.resize(256, 256)
# win.setWindowTitle('manual MIDA')

# app.setStyle("Fusion")
# palette = QPalette()
# palette.setColor(QPalette.Window, QColor(53, 53, 53))
# palette.setColor(QPalette.WindowText, Qt.white)
# app.setPalette(palette)
# win.show()

# label = QLabel('Hello World')
# label.show()
# app.exec_()