import numpy as np
import pandas as pd 

df = pd.read_excel('aa_info.xlsx')

def get_formula(seq,data):

	element_list = ['H', 'C', 'N', 'O', 'S']
	formula_dict = {element_list[i]: 0 for i in range(len(element_list))}

	for aa in seq:
		for element in element_list:
			formula_dict[element] += int(data[element].iloc[np.where(data['AA'] == aa)[0][0]])


	return [formula_dict[element] for element in list(formula_dict.keys())]

print(get_formula('AAA',df))