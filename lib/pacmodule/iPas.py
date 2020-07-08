#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def cal_pas(matfile, outfile):
    '''
    Description
    -----------
    Calculate protein activity score using gene expression data.
    For a data matrix with rows represent genes and columns represent samples (patients),
    This module calculate protein activy as follows:

        1) Remove any genes with missing values
        2) Standardrize gene expression values into Z-score
        3) Summerize Z-scores for each sample
        4) Normalize summerized Z-scores between [0,100]    
    
    Parameters
    ----------
    matfile : str
        mat file is Tab separated plain text file contaning Z-transformed gene expression scores
    outfile : str
        Ouput file contaning pas score
    '''
	
    print("\tReading matrix file: \"%s\" ..." % (matfile))
    df1 = pd.read_csv(matfile, index_col = 0, header=0, sep="\t")
    all_samples = df1.columns
    #remove NAs
    df2 = df1.dropna(axis=0, how='any')
    print("\t%d rows with missing values were removed." % (len(df1) - len(df2)))	
	
	
	### calcualte PAS score
    #key is sample ID, value is sum of Z-score
    pas_scores = {}
    #pas scores are normalized into [0,100]
    n_pas_scores = {}
    for s in all_samples:
        pas_scores[s] = df2[s].sum()
    min_pas = min(pas_scores.values())
    max_pas = max(pas_scores.values())
    range_pas = max_pas - min_pas
    for k,v in pas_scores.items():
        n_pas_scores[k] = (v - min_pas)*100/(range_pas)
    
    #print out normalized pas score   
    #for s in all_samples:
    #    print (s + '\t' + str(n_pas_scores[s]), file=OUT)
    pas = pd.Series(n_pas_scores)



	
	### perform PCA analysis
    print("\tTransposing data frame ...")
    df2 = df2.T
    #print (df2.head()) 
    
    print("\tStandarizing values ...")
    x = df2.values
    x = StandardScaler().fit_transform(x)
            
    pca = PCA(n_components = 2, random_state = 0)
    principalComponents = pca.fit_transform(x)  
    pca_names = ['PC1', 'PC2']
    principalDf = pd.DataFrame(data = principalComponents, columns = pca_names, index = df2.index)  

    principalDf['CES'] = pas    
    principalDf.index.name = 'sample_ID'
    #finalDf = pd.concat([principalDf, group], axis = 1, sort=True)
    #finalDf.index.name = 'sample_ID'
    
    print("\tWriting PCA results to file: \"%s\" ..." % (outfile))
    principalDf.to_csv(outfile, sep="\t")
    
        