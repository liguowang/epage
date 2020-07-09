#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 10:04:05 2019

@author: m102324

Description
-----------
This program Calculates the Composite Expression Scores:
	* Gene Set Variation Analysis (GSVA). (Hänzelmann et al, 2013)
	* Single Sample GSEA (ssGSEA).  (Barbie et al, 2009)
	* zscore (Lee et al, 2008)
	* plage (Tomfohr et al, 2005)
"""
import sys
#import numpy as np
#import pandas as pd
from time import strftime
import pandas as pd
from optparse import OptionParser
from pacmodule import iList,iMatrix,iPas,gsva,cpca

__author__ = "Liguo Wang"
__copyright__ = "Copyleft"
__credits__ = []
__license__ = "MIT"
__version__="1.0.0"
__maintainer__ = "Liguo Wang"
__email__ = "wang.liguo@mayo.edu"
__status__ = "Development"

def main():
	usage="%prog [options]" + "\n"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-e","--expr_matrix",action="store",type="string",dest="expr_file",help="Tab-separated data matrix file containing gene expression values. The 1st row containing sample/patient IDs and the 1st column containing gene symbols(mut be unique). File can be compressed (.gz, .Z, .z, .bz, .bz2, bzip2).")
	parser.add_option("-g","--gene",action="store",type="string",dest="gene_file",help="GMT file. The GMT file format is a tab delimited file format that describes gene sets (Each gene set is described by a name, a description, and the genes in the gene set). In the GMT format, each row represents a gene set. The first column is get set name (must be unique). The second column is brief description (can be 'na').")
	parser.add_option("-k","--group",action="store",type="string",dest="group_file",help="Group file (in CSV format). First column is sample ID, second column is group ID")
	parser.add_option("-s","--sample",action="store",type='string', dest="sample_file",default=None, help="Sample list file containing sample IDs. Each row can be a single sample ID, a comma-separated sample IDs or a space-separated sample IDs. Sample IDs must match exactly to those in the data matrix file. If omitted, calculated activity scores for *all* the samples. File can be compressed (.gz, .Z, .z, .bz, .bz2, bzip2). default=%default (All samples will be used)")
	parser.add_option("-l","--log",action="store_true",default=False,dest="log2",help="If True, will do log2(x+1) transformation for gene experssion values. Must set to 'True' if expressin values are RNA-seq count. default=%default")
	parser.add_option("-p","--processor",action="store", type='int',default=0,dest="n_thread",help="Number of processors to use when doing the calculations in parallel. default=%default (use all available processors)")
	parser.add_option("-o","--output",action="store",type='string', dest="out_file",help="The prefix of the output file.")
	

	(options,args)=parser.parse_args()
	 
	
	if not (options.expr_file):
		print ("-e/--expr_matrix: gene expression file must be specified.", file=sys.stderr)
		parser.print_help()
		sys.exit()
	if not (options.gene_file):
		print ("-g/--gene GMT file must be specified.", file=sys.stderr)
		parser.print_help()
		sys.exit()
	if not (options.out_file):
		print ("-o/--output: output prefix must be specified.", file=sys.stderr)
		parser.print_help()
		sys.exit()

	if not (options.group_file):
		print ("-k/--group: group must be specified.", file=sys.stderr)
		parser.print_help()
		sys.exit()
		
	# read gene set(s)
	print ("@ " + strftime("%Y-%m-%d %H:%M:%S : ") + "Read gene list from GMT file \"%s\" ..." % options.gene_file)
	gene_sets = iList.get_list(options.gene_file)
	all_genes = []	# combine gene sets
	print ("\tTotal %d gene sets loaded." % len(gene_sets), file=sys.stderr)
	for k in gene_sets:
		print ("\tGene set '%s': Total genes =  %d, Unique genes = %d" % (k, len(gene_sets[k]), len(set(gene_sets[k]))), file=sys.stderr)
		for g in gene_sets[k]:
			print ("\t" + g)
		all_genes += gene_sets[k]
	all_genes = list(set(all_genes))
   
   
   # read sample list
	sample_list = []
	if (options.sample_file):
		print ("@ " + strftime("%Y-%m-%d %H:%M:%S : ") + "Read sample list from \"%s\" ..." % options.sample_file)	
		sample_list = iList.get_list(options.sample_file)
		print ("\tTotal %d samples loaded." % len(sample_list))
		iList.print_list(sample_list)
	else:
		print ("@ " + strftime("%Y-%m-%d %H:%M:%S : ") + "Calculate activity score for **all samples** in \"%s\"" % options.expr_file)
	
	# read gene expression matrix
	print ("@ " + strftime("%Y-%m-%d %H:%M:%S : ") + "Read gene expression matrix from \"%s\" ..." % options.expr_file)
	genes_not_found = iMatrix.read_matrix(infile = options.expr_file, g_list = all_genes, s_list = sample_list, outfile = options.out_file + '.mat.tsv', zfile = None,log = options.log2)
	
	# run PCA
	print ("@ " + strftime("%Y-%m-%d %H:%M:%S : ") + "Calculate the first two principal components (saved to '%s') ..." % ((options.out_file + '_pca.csv')))
	cpca.run_PCA(options.out_file + '.mat.tsv', options.out_file)
	
	# rebuild GMT file by removing unfound genes
	if len(genes_not_found) > 0:
		print ("@ " + strftime("%Y-%m-%d %H:%M:%S : ") + "Rebuild GMT file as \"%s\" ..." % (options.out_file + '.New.gmt'))
		iList.rebuild_gmt(oldfile = options.gene_file, newfile = options.out_file + '.New.gmt', genes = genes_not_found)
		
		print ("@ " + strftime("%Y-%m-%d %H:%M:%S : ") + "Calculate GSVA (saved to '%s'), ssGSEA (saved to '%s'), Z-SCORE (saved to '%s') and PLAGE (saved to '%s') ..." % ((options.out_file + '_gsva.csv'), (options.out_file + '_ssgsea.csv'), (options.out_file + '_zscore.csv'), (options.out_file + '_plage.csv')))
		gsva.run_gsva(routfile = options.out_file + '.R', gmtfile = options.out_file + '.New.gmt', expr_file = options.out_file + '.mat.tsv', outfile = options.out_file, n_proc = options.n_thread)

	else:
		print ("@ " + strftime("%Y-%m-%d %H:%M:%S : ") + "Calculate GSVA (saved to '%s'), ssGSEA (saved to '%s'), Z-SCORE (saved to '%s') and PLAGE (saved to '%s') ..." % ((options.out_file + '_gsva.csv'), (options.out_file + '_ssgsea.csv'), (options.out_file + '_zscore.csv'), (options.out_file + '_plage.csv')))
		gsva.run_gsva(routfile = options.out_file + '.R', gmtfile = options.gene_file, expr_file = options.out_file + '.mat.tsv', outfile = options.out_file, n_proc = options.n_thread)
	
	
	
	
	# combine
	df_group = pd.read_csv(options.group_file,index_col = 0)
	df_gsva = pd.read_csv(options.out_file + '_gsva.csv',index_col = 0)
	df_ssgsea = pd.read_csv(options.out_file + '_ssgsea.csv',index_col = 0)
	df_zscore = pd.read_csv(options.out_file + '_zscore.csv',index_col = 0)
	df_plage = pd.read_csv(options.out_file + '_plage.csv',index_col = 0)
	df_pca = pd.read_csv(options.out_file + '_pca.csv',index_col = 0)
	
	data_frames = pd.concat([df_group, df_gsva, df_ssgsea,df_pca, df_zscore, df_plage],axis=1, join='inner')
	data_frames.to_csv(options.out_file + '_combined.tsv', index=True, sep="\t")
	
	#data_frames = pd.concat([df_gsva, df_ssgsea,df_zscore, df_plage],axis=1, join='inner')
	#data_frames.to_csv(options.out_file + '_combined.tsv', index=True,sep="\t")
	
if __name__=='__main__':
	main()
			
