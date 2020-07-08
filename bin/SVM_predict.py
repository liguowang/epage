#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 09:14:42 2020

@author: m102324

Description
-----------
Build SVM model from "train_file" and then predict cases in "data_file"

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
from pacmodule.svm import svm_predict

__author__ = "Liguo Wang"
__copyright__ = "Copyleft"
__credits__ = []
__license__ = "GPL"
__version__="1.0.0"
__maintainer__ = "Liguo Wang"
__email__ = "wang.liguo@mayo.edu"
__status__ = "Development"

	
def main():
	
	usage="%prog [options]" + "\n"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-t","--train_file",action="store",type="string",dest="train_file",help="Tab or space separated file (for tranining purpose, to build SVM model). The first column contains *sample IDs*; the second column contains *sample labels* in integer (must be 0 or 1); the third column contains *sample label names* (string, must be consistent with column-2). The remaining columns contain featuers used to build SVM model. ")
	parser.add_option("-d","--data_file",action="store",type="string",dest="data_file",help="Tab or space separated file (new data to predict the label). The first column contains *sample IDs*; the second column contains *sample labels* in integer (must be 0 or 1); the third column contains *sample label names* (string, must be consistent with column-2). The remaining columns contain featuers used to build SVM model. ")
	parser.add_option("-C","--cvalue",action="store",type='float', dest="C_value", default=1.0, help="C value. default=%default")
	parser.add_option("-k","--kernel",action="store",type='string', dest="s_kernel", default='linear', help="Specifies the kernel type to be used in the algorithm. It must be one of ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’ or a callable. If none is given, ‘rbf’ will be used. default=%default")	
	(options,args)=parser.parse_args()
	
	print ()
	if not (options.train_file):
		print (__doc__)
		parser.print_help()
		sys.exit(101)
	if not (options.data_file):
		print (__doc__)
		parser.print_help()
		sys.exit(101)
	if options.s_kernel not in ('linear', 'poly', 'rbf', 'sigmoid', 'precomputed'):
		print ("'-k' must be one of ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’.")
		parser.print_help()
		sys.exit(102)
	
	svm_predict(train_file = options.train_file, data_file = options.data_file,C_value = options.C_value,  krnl = options.s_kernel)

if __name__=='__main__':
	main()	