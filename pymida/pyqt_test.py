import sys
import os 
import numpy as np
import pandas as pd 

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from PyQt5.uic import *


class MainWindow(QtWidgets.QMainWindow):

	def __init__(self,parent = None):

		QMainWindow.__init__(self,parent)

		self.show()





def main():

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())

main()