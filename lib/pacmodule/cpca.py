#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 17:28:59 2019

@author: m102324
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from time import strftime

def run_PCA(infile, outfile):
	print ("@ " + strftime("%Y-%m-%d %H:%M:%S : ") + "Read input file \"%s\" ..." % infile)
	df1 = pd.read_csv(infile, index_col = 0, sep="\t")
	
	#remove NA and transpose
	df2 = df1.dropna(axis=0, how='any')
	print ("@ " + strftime("%Y-%m-%d %H:%M:%S : ") + "%d rows with missing values were removed." % (len(df1) - len(df2)))
	
	print ("@ " + strftime("%Y-%m-%d %H:%M:%S : ") + "ransposing data frame ...")
	df2 = df2.T
	
	print ("@ " + strftime("%Y-%m-%d %H:%M:%S : ") + "standarizing values")
	x = df2.values
	x = StandardScaler().fit_transform(x)
	 
	pca = PCA(n_components = 2, random_state = 0)	 
	principalComponents = pca.fit_transform(x)
	pca_names = [str(i)+str(j) for i,j in zip(['PC']*2,range(1,3))]
	principalDf = pd.DataFrame(data = principalComponents, columns = pca_names, index = df2.index)
	#principalDf.index.name = 'Sample_ID'
	
	print ("@ " + strftime("%Y-%m-%d %H:%M:%S : ") + "Writing PCA results to file: \"%s\" ..." % (outfile + '_pca.csv'))
	principalDf.to_csv(outfile + '_pca.csv')