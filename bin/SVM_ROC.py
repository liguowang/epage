#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 09:29:30 2019
@author: m102324

Description
-----------
Plot Receiver operating characteristic (ROC) curves using K-fold cross-validation.

Format
-------
* 1st-column : sample ID (string)
* 2nd-column : binary label (intger, must be 0 or 1)
* 3rd-column : label name (string, must be consistent with label)
* 4th-column -  : featuers used to build SVM model

Example of input data file
--------------------------
ID  Label   Label_name  feature_1   feature_2   feature_3    ...
sample_1    1   WT  1560    795 0.9716    ...
sample_2    1   WT  784 219 0.4087    ...
sample_3    1   WT  2661    2268    1.1691    ...
sample_4    0   Mut 643 198 0.5458    ...
sample_5    0   Mut 534 87  1.0545    ...
sample_6    0   Mut 332 75  0.5115    ...
...
	
"""


import sys
from optparse import OptionParser
from pacmodule.svm import plot_cvROC

__author__ = "Liguo Wang"
__copyright__ = "Copyleft"
__credits__ = []
__license__ = "GPL"
__version__="1.0.0"
__maintainer__ = "Liguo Wang"
__email__ = "wang.liguo@mayo.edu"
__status__ = "Development"

def pick_colors(n):
	my_colors = ['#e6194B', '#3cb44b', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabebe', '#469990', '#e6beff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9','#ffe119']
	if n > len(my_colors):
		print ("Only support 21 different colors", file = sys.stderr)
		sys.exit()
	return my_colors[0:n]

	
def main():
	
	usage="%prog [options]" + "\n"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-i","--input_file",action="store",type="string",dest="input_file",help="Tab or space separated file. The first column contains *sample IDs*; the second column contains *sample labels* in integer (must be 0 or 1); the third column contains *sample label names* (string, must be consistent with column-2). The remaining columns contain featuers used to build SVM model. ")
	parser.add_option("-o","--output",action="store",type='string', dest="out_file",help="The prefix of the output file.")
	parser.add_option("-n","--nfold",action="store",type="int",dest="n_fold",default=5,help="The original sample is randomly partitioned into *n* equal sized subsamples (2 =< n <= 10). Of the n subsamples, a single subsample is retained as the validation data for testing the model, and the remaining n − 1 subsamples are used as training data. default=%default.")
	parser.add_option("-C","--cvalue",action="store",type='float', dest="C_value", default=1.0, help="C value. default=%default")
	parser.add_option("-s","--seed",action="store",type='int', dest="rand_seed", default=0, help="random_state seed used by the random number generator. default=%default")
	parser.add_option("-k","--kernel",action="store",type='string', dest="s_kernel", default='linear', help="Specifies the kernel type to be used in the algorithm. It must be one of ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’ or a callable. If none is given, ‘rbf’ will be used. default=%default")
	parser.add_option("--xl",action="store",type="float",dest="x_low",default=-0.05, help="The lower limit of X-axis (false positive rate). default=%default")
	parser.add_option("--xu",action="store",type="float",dest="x_upper",default=0.5, help="The upper limit of X-axis (false positive rate). default=%default")
	parser.add_option("--yl",action="store",type="float",dest="y_low",default=0.5, help="The lower limit of Y-axis (true positive rate). default=%default")
	parser.add_option("--yu",action="store",type="float",dest="y_upper",default=1.05, help="The upper limit of Y-axis (true positive rate). default=%default")	
	
	
	
	(options,args)=parser.parse_args()
	
	print ()
	if not (options.input_file):
		print (__doc__)
		parser.print_help()
		sys.exit(101)
	
	if not (options.out_file):
		print (__doc__)
		parser.print_help()
		sys.exit(103)	
	if options.n_fold > 10:
		options.n_fold = 10
	if options.n_fold < 2:
		options.n_fold = 2
	if options.x_low < -0.05:
		options.x_low = -0.05
	if options.x_upper > 1.05:
		options.x_upper = 1.05
	if options.y_low < -0.05:
		options.y_low = -0.05
	if options.y_upper > 1.05:
		options.x_upper = 1.05
	
	plot_cvROC(infile = options.input_file, xl=options.x_low, xu=options.x_upper, yl=options.y_low, yu=options.y_upper, k=options.n_fold, C_value = options.C_value, seed=options.rand_seed,krnl=options.s_kernel,outfile=options.out_file)
		
		
		
if __name__=='__main__':
	main()		
		
		
		
		
		
		
		
		
		
		
		
		