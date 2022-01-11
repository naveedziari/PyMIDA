import sys
import os 
import numpy as np
import pandas as pd 

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from PyQt5.uic import *

from mida_alg import Abundance
import __main__


#https://stackoverflow.com/questions/48070224/pyqt5-how-to-use-slotsignal-in-different-classes




class Peptide(QtWidgets.QMainWindow):

	def __init__(self, parent = None):

		QMainWindow.__init__(self,parent)
		uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)),'peptide_ui.ui'), self)
		self.setWindowTitle('Peptide Calculator')
		self.show()

		self.df = pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aa_info.xlsx'))

		self.peptide_retrieve = self.findChild(QLineEdit, 'peptide_seq')

		self.main_window = MainWindow()

		temp_push = self.findChild(QPushButton, 'peptide_calc')
		#temp_push.clicked.connect(self.get_formula)
		temp_push.clicked.connect(self.populate_main_window)
		temp_push.clicked.connect(self.close)

		
	def populate_main_window(self):

		self.main_window = MainWindow()
		self.main_window.num_labile_input.setText(self.get_n)




	def get_peptide_seq(self):

		#print(str(self.peptide_retrieve.text()))
		return str(self.peptide_retrieve.text())


	def get_n(self,seq,df):

		n = 0
		for aa in seq:
			n += int(df['n'].iloc[np.where(df['AA'] == aa)[0][0]])

		return n

	def get_formula(self,seq,df):

		element_list = ['H', 'C', 'N', 'O', 'S']
		formula_dict = {element_list[i]: 0 for i in range(len(element_list))}

		for aa in seq:
			for element in element_list:
				formula_dict[element] += int(df[element].iloc[np.where(df['AA'] == aa)[0][0]])


		return [formula_dict[element] for element in list(formula_dict.keys())]

		
	def get_info(self):


		pep_seq = self.get_peptide_seq()
		temp_n = self.get_n(pep_seq,self.df)
		temp_formula  = self.get_formula(pep_seq,self.df)
		print(temp_formula)


		self.close()

		return [temp_n,temp_formula]
	
