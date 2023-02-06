from pyteomics import mzml, auxiliary
import numpy as np
import pandas as pd 


# with mzml.read(open('1HM_MDM000322_HeartSDS_D10 Days_MS_rep1Q4-27Pxxx.mzML')) as reader:
#     auxiliary.print_tree(next(reader))

#reader.close()


with mzml.read('1HM_MDM000322_HeartSDS_D10 Days_MS_rep1Q4-27Pxxx.mzML') as reader:
	raw_data = list(reader)
reader.close()

# for line in raw_data:
# 	print(line)


print(raw_data[8]['intensity array'])