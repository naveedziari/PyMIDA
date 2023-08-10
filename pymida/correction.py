import numpy as np 


def normalization(iso_dist):
	print(iso_dist.ndim)
	if iso_dist.ndim == 1:
		output = iso_dist/np.sum(iso_dist)
	else:
		output = np.zeros(iso_dist.shape)
		for row_index in range(iso_dist.shape[0]):
			output[row_index,:] = [iso_dist[row_index,col_index]/np.sum(iso_dist[row_index,:]) for col_index in range(iso_dist.shape[1])]
	return output

