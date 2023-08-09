# PyMIDA

PyMIDA is a graphical user interface python package that allows users to perform mass isotopomer distribution analysis (MIDA). 

This program can calculate the fraction of newly synthesized molecules, the turnover rate of polymers, the isotopic enrichment of the precursor pool, and the number of atoms that are replaced or exchanged during metabolic processes. 

NOTE: this software was developed on Windows 10 and also tested on Intel-based Mac OS using Python 3.9.6. The newest version of Python 3 (3.11.x) has new type for the **self** keyword and may lead to compilation error. Please report any bugs or malfunctions to (mailto:naveedziari@berkeley.edu).
 
# Installation and Requirements

This package requires Python 3.x and has the following codependencies:
* numpy
* scipy
* pandas
* PyQT5

To run the program,  download the `pymida` folder, go to its directory in the command line and run `python pymida` (or whatever command is used to invoke Python 3.x). This window will pop up:

<img width="512" alt="pymida_screenshot" src="https://github.com/naveedziari/PyMIDA/assets/14845065/ae468725-b558-4c81-b72c-85b691831534">


# Parameters

* Formula: input the number of atoms found in the molecule under analysis. Any field left blank will register a zero.
* Labeled isotope: select the stable isotope that is experimentally enriched (deuterium, carbon-13, nitrogen-15)
* Enrichment: define the isotopic enrichment of the precursor pool
   * p: the isotopic enrichment of the precursor pool, with  acceptable range (0,1)
   * number of labile bonds: the number of atoms of the labeled isotope that are exchange during the metabolic process (n)
 * Display:
   * increment: The increment at which each row on the MIDA table is displayed. For instance, if p is defined as 0.05 and increment as 0.01, then it will display distributions for p= 0, 0.01, 0.02, 0.03, 0.04, 0.05. Must be a factor of p (e.g. p = 0.05 and increment = 0.02 will throw an error because 0.05 % 0.02 != 0).
   * number of isotopomers: Specify the number of isotopomers to normalize (correct such that the sum of the distribution is equal to one), and to display on the MIDA table (e.g. if user specifies 4, then it will display isotopomers M0, M1, M2, and M3). Must a positive integer value.

For generation of the MIDA table, user can choose to copy to a clipboard to paste into any spreadsheet program or to write it to a `.csv` file.


<img src="https://user-images.githubusercontent.com/14845065/152647299-d9c993fe-55ad-4fb5-8928-9c7b165f0784.jpg" alt="drawing" width="384"/>

In addition, if the user wants to analyze a peptide, then under the `windows` tab select `Proteomics` to be prompted with a window to enter the peptide amino acid sequence:

<img src="https://user-images.githubusercontent.com/14845065/152647318-79157d76-94f5-4962-a4df-d3c35db8291a.jpg" alt="drawing" width="384"/>

# Calculation of isotopic enrichment and fractional synthesis rate.

* The user may also input experimentally derived fractional abundances into the fields labeled **M0-M4**. At minimum M0-M2 must be populated, and the number of isotopomers specified above must match the number inputted here. 
* Then click on **Calculate MIDA p** and a window will pop up displaying the isotopic enrichment of the precursor pool. This step is necessary in order to calculate $f$.
* After calculating $p$, clicking on **Calculate f** will open up a new window whereby the user can select the mass isotopomer with which to calculate $f$. 
*Proceed with steps below to calculate FSR*
* Input the timepoint at which the measurement was taken, with time point zero being the start of labeling. 
* Click on **Calculate FSR** to display the fractional synthesis rate.
* 
<img width="635" alt="fraction_screenshot" src="https://github.com/naveedziari/PyMIDA/assets/14845065/721d8b07-4eaf-42d6-87ef-dd416a5889a1">



