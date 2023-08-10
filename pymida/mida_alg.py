import numpy as np 
import re
import scipy.special 
import itertools
import pandas as pandas

from numeric_functions import binnings

DEFAULT_CUTOFF = 15

class Abundance():

	def __init__(self,formula,num_labile = 0, p = 0, heavy_element = 'hydrogen'):


		self.heavy_element = heavy_element

		self.isotopes = [
			(0.999844, 0.000156), #hydrogen
			(0.9891, 0.0109), #carbon
			(0.99635,0.00365), #nitrogen
			(0.99759,0.00037,0.00204), #oxygen
			(0.9493,0.0076,0.0429,0.0002), #sulfur
			(1.0, 0), #phosphorus
			(0.92223, 0.04685, 0.03092) #silicon
			]

		self.p = p
		self.num_labile = num_labile

		# self.formula_str = formula_strz

		# self.formula = [int(s[1:]) for s in re.sub(r"(\w)([A-Z])", r"\1 \2", formula_str).split(' ')]

		self.formula = formula

		if self.num_labile != 0:

			heavy_element_list = ['hydrogen', 'carbon', 'nitrogen']
			element_index = heavy_element_list.index(self.heavy_element)

			for i,element_num in enumerate(self.formula):
				if i == element_index:
					self.formula = self.formula[:i] + [self.num_labile] + [self.formula[i] - self.num_labile] + self.formula[(i+1):]
					labile_enrichments = tuple([self.isotopes[i][0] - self.p, self.isotopes[i][1]+self.p])
					self.isotopes = self.isotopes[:i] + [labile_enrichments] + self.isotopes[i:]

			# num_hydrogen = self.formula[0]
			# self.formula = [self.num_labile] + [self.formula[0] - self.num_labile] + self.formula[1:]
			# labile_enrichments = tuple([self.isotopes[0][0]-self.p,self.isotopes[0][1]+self.p])
			# self.isotopes = [labile_enrichments] + self.isotopes

		self.isotopes = np.asarray(self.isotopes)

	def elemental_distribution(self,num_atoms,abundances):
		combos = binnings(num_atoms,len(abundances))
		coeffs = np.zeros(combos.shape)
		for i in range(len(abundances)): 
			coeffs[:,i] = combos[:,0:(i+1)].sum(axis=1)
		mn_coeffs = scipy.special.comb(coeffs,combos).prod(axis=1)
		#print(abundances)
		if len(abundances.shape) == 1:
			return np.array([mn_coeffs * (abundances**combos).prod(axis=1)])
		else:
			return mn_coeffs * (abundances[:, np.newaxis]**combos[np.newaxis, :]).prod(axis=2)


	def molecular_distribution(self,distributions):
		max_mass_bins = 15
		for i,dist in enumerate(distributions):
			if i == 0:
				total_dist = dist
				continue
			total_dist_size = total_dist.shape[1]
			dist_size = min(max_mass_bins, dist.shape[1])
			new_dist_size = min(max_mass_bins, total_dist_size + dist_size - 1)
			num_enrichments = max(dist.shape[0], total_dist.shape[0])
			new_dist = np.zeros((num_enrichments, new_dist_size))
			for i in range(total_dist_size):
				for j in range(dist_size):
					mass = i + j
					if mass < new_dist_size: 
						new_dist[:, mass] += total_dist[:, i] * dist[:, j]
					else: 
						break  
			total_dist = new_dist
		return total_dist

	def get_MID(self):

		distributions = []
		for i in range(len(self.formula)):
			dist_append = self.elemental_distribution(self.formula[i],np.array(self.isotopes[i]))
			distributions.append(dist_append)

		return self.molecular_distribution(distributions)

# def main():

# 	p = 0.05
# 	num_labile = 0
# 	chemical_formula = 'H100C56N16O18S0'
# 	chemical_formula = 'H8C8N0O0S0'
# 	x = Abundance(chemical_formula, num_labile, p, 'carbon')
# 	isotopoomer_distribution = x.get_MID()
# 	print(isotopoomer_distribution)

# main()


#add silicon and phosphorus