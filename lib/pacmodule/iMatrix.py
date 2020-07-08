#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 11:47:21 2019

@author: m102324
"""
import sys
import math
from pacmodule import iReader
from scipy import stats

def read_matrix(infile, g_list, s_list, outfile, zfile,log=False):
    '''
    Slice a subset from matrix file.
    
    Parameters
    ----------
    infile : str
        Input matrix file.
    g_list : list
        List containing gene symbols. Symbols not contained in infile will be 
        skipped.
    s_list : list
        List containing sample IDs. IDs not contained in infile will be skipped.
    outfile : str
        Output file containing the orignal gene expression scores.
    zfile : str
        Output file containing Z-scores.
    log : bool
        If ture, we will do log2(x+1) transformation for expression values. 
    '''
    
    OUT = open(outfile, 'w')
    if zfile is not None:
        ZOUT = open(zfile, 'w')
    g_list = set(g_list)
    s_list = set(s_list)
    genes_not_found = []
	
    line_num = 0
    genes_found = set()
    for l in iReader.reader(infile):
        l = l.strip()
        line_num += 1
        if line_num == 1:
            all_samples = l.split()[1:]
            
            #output a subset of samples
            if len(s_list) > 0:
                subset_index = []
                for i in range(0,len(all_samples)):
                    if all_samples[i] in s_list:
                        subset_index.append(i)
            
                subset_samples = [all_samples[i] for i in subset_index]
                print ('sample\t' + '\t'.join(subset_samples), file=OUT)
                if zfile is not None:
                    print ('sample\t' + '\t'.join(subset_samples), file=ZOUT)
            #output all samples
            else:
                print ('sample\t' + '\t'.join(all_samples), file=OUT)
                if zfile is not None:
                    print ('sample\t' + '\t'.join(all_samples), file=ZOUT)
        else: 
            tmp = l.split()
            geneID = tmp[0]
            if len(g_list) > 0:
                if geneID not in g_list:
                    continue
                genes_found.add(geneID)
            
            #convert str into floats
            try:
                all_scores = list(map(float,tmp[1:]))
            except:
                print ("Skip line with missing values:" + l, file=sys.stderr)
                continue
            
            #do log2(x+1) transformation
            if log:
                all_scores = [math.log2(i+1) for i in all_scores]
            
            if len(s_list) > 0:
                subset_scores = [all_scores[i] for i in subset_index]
                print (geneID + '\t' + '\t'.join([str(i) for i in subset_scores]), file=OUT)
                if zfile is not None:
                    subset_z_scores = stats.zscore([i for i in subset_scores])
                    print (geneID + '\t' + '\t'.join([str(i) for i in subset_z_scores]), file=ZOUT)
            else:
                print (geneID + '\t' + '\t'.join([str(i) for i in all_scores]), file=OUT)
                if zfile is not None:
                    all_z_scores = stats.zscore([i for i in all_scores])
                    print (geneID + '\t' + '\t'.join([str(i) for i in all_z_scores]), file=ZOUT)
    
    if len(g_list) > 0:
        genes_not_found = list(g_list - genes_found)
        if len(genes_not_found) > 0:
            print ("\t%d Genes not found:" % len(genes_not_found), genes_not_found)
        else:
            print ("\tAll the genes were found.")
    OUT.close()
    return genes_not_found
   
   