import sys
import os 
import numpy as np
import pandas as pd
import warnings
import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from PyQt5.uic import *

from decimal import Decimal

from mida_alg import Abundance
#from peptide_calc import Peptide
from correction import normalization

'''
to do list
-add silicon and phosphorus
-EM values and ratios
-MIT vs apache license
-add rows (nominal mass, exact mass) like isotopomer program
-cannot have greater number of label than formula
'''

'''
PROTEOMICS:
-why is cysteine IAM modified and not by itself
-why is methionine oxidized
'''

#https://stackoverflow.com/questions/15829782/how-to-restrict-user-input-in-qlineedit-in-pyqt


location =  os.path.dirname(os.path.abspath(__file__))



if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

#QT_AUTO_SCREEN_SCALE_FACTOR=2 


#QGuiApplication().setAttribute(Qt.AA_DisableHighDpiScaling)


class Peptide(QtWidgets.QMainWindow):

	def __init__(self, parent = None):

		QMainWindow.__init__(self,parent)
		uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)),'peptide_ui.ui'), self)
		self.setWindowTitle('Peptide Calculator')
		#self.show()

		self.df = pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aa_info.xlsx'))

		self.peptide_retrieve = self.findChild(QLineEdit, 'peptide_seq')

		self.main_window = MainWindow()
		self.show()

		temp_push = self.findChild(QPushButton, 'peptide_calc')
		#temp_push.clicked.connect(self.get_formula)
		temp_push.clicked.connect(self.populate_main_window)
		temp_push.clicked.connect(self.close)

		
	def populate_main_window(self):

		self.main_window = MainWindow()
		self.main_window.num_labile_input.setText(str(self.get_n(self.get_peptide_seq(),self.df)))

		formula = self.get_formula(self.get_peptide_seq(),self.df)
		self.main_window.h_input.setText(str(formula[0]))
		self.main_window.c_input.setText(str(formula[1]))
		self.main_window.o_input.setText(str(formula[2]))
		self.main_window.n_input.setText(str(formula[3]))
		self.main_window.s_input.setText(str(formula[4]))


	def get_peptide_seq(self):

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
			#removal of water
		num_water = len(seq) - 1
		formula_dict['H'] -= 2*num_water
		formula_dict['O'] -= num_water

		return [formula_dict[element] for element in list(formula_dict.keys())]


class Fraction(QtWidgets.QMainWindow):

	def __init__(self,data_frame, parent = None):

		QMainWindow.__init__(self,parent)
		uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)),'fraction_ui.ui'), self)
		self.setWindowTitle('FSR calculator')

		self.m0 = self.findChild(QRadioButton, 'M0_select')
		self.m1 = self.findChild(QRadioButton, 'M1_select')
		self.m2 = self.findChild(QRadioButton, 'M2_select')

		self.abundance = self.findChild(QLineEdit,'normalized_abundance')
		self.time = self.findChild(QLineEdit,'fsr_timepoint')


		self.data = data_frame
		self.labeling_pattern = self.data.iloc[-1]
		self.natural_abundance = self.data.iloc[0]
		df_length = len(self.labeling_pattern)-1
		self.labeling_pattern = self.labeling_pattern[-df_length:]

		self.lcd_f = self.findChild(QLCDNumber,'display_f')
		self.lcd_fsr = self.findChild(QLCDNumber, 'display_fsr')
		f_push = self.findChild(QPushButton,'f_calc_button')
		f_push.clicked.connect(self.calc_f)
		fsr_push = self.findChild(QPushButton, 'FSR_calc_button')
		fsr_push.clicked.connect(self.calc_fsr)

	def get_isotopomer(self):

		self.isotopomer = 1

		if self.m0.isChecked(): 
			self.isotopomer = 0
		if self.m1.isChecked():
			self.isotopomer = 1
		if self.m2.isChecked():
			self.isotopomer = 2

		return self.isotopomer


	def calc_f(self):

		abundance = float(str(self.abundance.text()))
		index = self.get_isotopomer()
		enrichment = abundance - self.natural_abundance[index+1]
		f = float(enrichment/self.labeling_pattern[index+1])
		self.lcd_f.display(f)
		print(self.data)
		print(self.labeling_pattern[index+1])
		print(self.natural_abundance[index+1])
		print(enrichment)
		print(f)
		return f


	def get_time(self):

		return float(str(self.time.text()))

	def calc_fsr(self):

		k = -np.log(1-self.calc_f())/self.get_time()
		self.lcd_fsr.display(k)


class MainWindow(QtWidgets.QMainWindow):

	def __init__(self,parent = None):

		QMainWindow.__init__(self,parent)

		uic.loadUi(os.path.join(location,'main_ui.ui'),self)
		self.setWindowTitle('PyMIDA')


		formula_validator = QIntValidator(0, 1000, self)

		self.h_input = self.findChild(QLineEdit, 'h_input')
		self.c_input = self.findChild(QLineEdit, 'c_input')
		self.n_input = self.findChild(QLineEdit, 'n_input')
		self.o_input = self.findChild(QLineEdit, 'o_input')
		self.s_input = self.findChild(QLineEdit, 's_input')
		self.p_input = self.findChild(QLineEdit, 'p_input')
		self.si_input = self.findChild(QLineEdit, 'si_input')


		self.h_input.setValidator(formula_validator)
		self.c_input.setValidator(formula_validator)
		self.n_input.setValidator(formula_validator)
		self.o_input.setValidator(formula_validator)
		self.s_input.setValidator(formula_validator)
		self.p_input.setValidator(formula_validator)
		self.si_input.setValidator(formula_validator)


		self.enrichment = self.findChild(QLineEdit, 'enrichment_input')
		self.num_labile_input = self.findChild(QLineEdit, 'num_labile')


		self.increment_input = self.findChild(QLineEdit, 'increment')


		isotopomer_validator= QIntValidator(1,15,self)
		self.num_isotopomers = self.findChild(QLineEdit, 'num_isotopomers')
		self.num_isotopomers.setValidator(isotopomer_validator)


		self.h_label = self.findChild(QRadioButton, 'h_label')
		self.c_label = self.findChild(QRadioButton, 'c_label')
		self.n_label = self.findChild(QRadioButton, 'n_label')


		clipboard_push = self.findChild(QPushButton,'execute')

		clipboard_push.clicked.connect(self.create_table)

		#######

		csv_push = self.findChild(QPushButton, 'execute_2')

		csv_push.clicked.connect(self.create_csv)

		#######

		calc_f_push = self.findChild(QPushButton, 'calc_f')
		calc_f_push.clicked.connect(self.start_calc_f)


		q_exit = self.findChild(QAction, 'actionExit')
		q_exit.triggered.connect(self.exit_app)


		q_proteomics = self.findChild(QAction, 'actionProteomics')
		q_proteomics.triggered.connect(self.start_peptide)
		#q_proteomics.triggered.connect(self.close)
		self.peptide_bool = False


		self.show()


	def start_peptide(self):

		self.peptide_window = Peptide()
		self.peptide_window.show()
		self.close()

	def start_calc_f(self):

		df = self.create_table()

		
		self.f_window = Fraction(df)
		self.f_window.show()
		self.close()



	def get_formula(self):

		formula_list = [str(self.h_input.text()),str(self.c_input.text()), str(self.n_input.text()), str(self.o_input.text()), \
		 str(self.s_input.text()), str(self.p_input.text()), str(self.si_input.text())]

		output_list = []

		for i in formula_list:
			if not i: output_list.append(0)
			else: output_list.append(int(i))

		return output_list


	def get_label(self):

		self.label = ''

		if self.h_label.isChecked(): 
			self.label = 'hydrogen'
		if self.c_label.isChecked():
			self.label = 'carbon'
		if self.n_label.isChecked():
			self.label = 'nitrogen'

		return self.label

	def get_enrichment(self):

		if str(self.enrichment.text()):
			fct_output = float(str(self.enrichment.text()))
			return fct_output
		else:
			return 0

	def get_increments(self):

		output_list = []
		increment = float(str(self.increment.text()))
		num_iterations = int(self.get_enrichment()/increment)	

		for i in range(num_iterations+1):
			output_list.append(increment*i)

		return output_list

	def get_num_labile(self):

		if str(self.num_labile_input.text()):
			fct_output = int(str(self.num_labile_input.text()))
			return fct_output
		else:
			return 0

	def get_num_isotopomers(self):

		return int(self.num_isotopomers.text())

		#return float(self.num_isotopomers.text())

	def exit_app(self):

		sys.exit(app.exec_())
		return None


	def create_table(self):

		'''
		main function to call on MIDA to run and copy to clipboard
		'''

		formula = self.get_formula()
		num_labile = self.get_num_labile()
		enrichment = self.get_enrichment()
		label = self.get_label()
		increments = self.get_increments()

		remainder = Decimal(str(enrichment)) % Decimal(str(self.increment.text()))
		print(remainder != 0)

		# if self.retrieve_info:

		# 	num_labile = self.w.get_info()[0]
		# 	formula = self.w.get_info()[1]
		# 	complete_n = QCompleter()
		# 	self.num_labile_input(complete_n)
		# 	model = QStringListModel()
		# 	model.setStringList(str(num_labile))




		#error mesages

		if not label:
			QtWidgets.QMessageBox.information(self,"Error", "Please Select Label")

		if enrichment > 1.00:
			QtWidgets.QMessageBox.information(self,"Error", "The enrichment (p) must lie between 0 and 1")

		if Decimal(str(enrichment)) % Decimal(str(self.increment.text())) != 0:
			QtWidgets.QMessageBox.information(self,"Error", "The enrichment (p) must be divisible by the increment")


		if not self.get_num_isotopomers() or self.get_num_isotopomers == 0:
			QtWidgets.QMessageBox.information(self,"Error", "The number of isotopomers to display must be a positive integer")


		numpy_array = np.zeros((len(increments),15))


		nat_obj = Abundance(formula)
		nat_abundance_array = nat_obj.get_MID()
		numpy_array[0,:] = nat_abundance_array[0]

		for i,p_val in enumerate(increments[1:]):
			enrich_obj = Abundance(formula, num_labile, p = p_val, heavy_element = label)
			enrich_array = enrich_obj.get_MID()
			numpy_array[i+1,:] = enrich_array[0]

		abundance_array = numpy_array[:,:self.get_num_isotopomers()]
		abundance_array = normalization(abundance_array)


		enrichment_array = np.zeros(abundance_array.shape)
		enrichment_array[0,:] = np.nan
		for row_index in range(1,enrichment_array.shape[0]):
			enrichment_array[row_index,:] = [abundance_array[row_index,col_index] - abundance_array[0,col_index] for col_index in range(abundance_array.shape[1])]

		


		#df = pd.DataFrame(abundance_array)
		final_numpy_array = np.concatenate((abundance_array,enrichment_array),axis=1)
		df = pd.DataFrame(final_numpy_array)
		col_names = ['M'+str(i) for i in range(int(self.get_num_isotopomers()))]
		enrichment_col_names = ['EM'+str(i) for i in range(int(self.get_num_isotopomers()))]
		df.columns = col_names + enrichment_col_names
		df.insert(loc = 0, column = 'p', value = increments)


		
		df.to_clipboard(index = False, header = True, excel = True)

		return df

	def create_csv(self):

		'''
		main function to call on MIDA to run and create csv
		'''

		formula = self.get_formula()
		num_labile = self.get_num_labile()
		enrichment = self.get_enrichment()
		label = self.get_label()
		increments = self.get_increments()




		#error mesages

		if not label:
			QtWidgets.QMessageBox.information(self,"Error", "Please Select Label")

		if enrichment > 1.00:
			QtWidgets.QMessageBox.information(self,"Error", "The enrichment (p) must lie between 0 and 1")


		if Decimal(str(enrichment)) % Decimal(str(self.increment.text())) != 0:
			QtWidgets.QMessageBox.information(self,"Error", "The enrichment (p) must be divisible by the increment")

		if not self.get_num_isotopomers() or self.get_num_isotopomers == 0:
			QtWidgets.QMessageBox.information(self,"Error", "The number of isotopomers to display must be a positive integer")


		numpy_array = np.zeros((len(increments),15))


		nat_obj = Abundance(formula)
		nat_abundance_array = nat_obj.get_MID()
		numpy_array[0,:] = nat_abundance_array[0]

		for i,p_val in enumerate(increments[1:]):
			enrich_obj = Abundance(formula, num_labile, p = p_val, heavy_element = label)
			enrich_array = enrich_obj.get_MID()
			numpy_array[i+1,:] = enrich_array[0]

		abundance_array = numpy_array[:,:self.get_num_isotopomers()]
		abundance_array = normalization(abundance_array)


		df = pd.DataFrame(abundance_array, dtype = 'object')
		col_names = ['M'+str(i) for i in range(len(list(df.columns)))]
		df.columns = [col_names]
		df.insert(loc = 0, column = 'p', value = increments)


		output_file_name = 'temp.csv'
		user_input = QInputDialog.getText(self,'CSV file creation','Please enter output file name:')
		output_file_name = str(user_input[0] + '.csv')
		#add functionality for windows/mac file browser

		df.to_csv(output_file_name, index = False, header = True)




if __name__ == "__main__":

	
	app = QApplication(sys.argv[1:])


	# app.setStyle("Fusion")
	# palette = QPalette()
	# palette.setColor(QPalette.Window, QColor(8, 8, 100))
	# palette.setColor(QPalette.WindowText, Qt.white)
	# app.setPalette(palette)

	window = MainWindow()
	window.show()

	#peptide = Peptide()

	# main.btn_TrainSys.clicked.connect(lambda: changeWindow(window, peptide))
 #    trainsys.btn_Backtrain.clicked.connect(lambda: changeWindow(peptide, window))


	sys.exit(app.exec_())





	