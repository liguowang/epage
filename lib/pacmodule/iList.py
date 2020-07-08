# -*- coding: utf-8 -*-

from pacmodule import iReader
import collections

def get_list(infile):
	'''
	Get list from GMT file. The GMT file format is a tab delimited file format that
	describes gene sets. In the GMT format, each row represents a gene set
		
	parameters
	----------
	
	infile : str
		Input file in GMT format.
	
	Return
	------
	dict of list with geneset name as key, and list of gene symbols as value
	'''
	gene_sets = collections.defaultdict(list)
		
	for l in iReader.reader(infile):
		l = l.strip()
		if l.startswith('#'):continue
		f = l.split('\t')
		if len(f) < 3: continue
		gene_set_id = f[0]
		gene_names = f[2:]
		gene_sets[gene_set_id] = gene_names
	return gene_sets

def rebuild_gmt(oldfile, newfile, genes):
	OUT = open(newfile,'w')
	for l in iReader.reader(oldfile):
		l = l.strip()
		if l.startswith('#'):continue
		f = l.split('\t')
		if len(f) < 3: continue
		gene_set_id = f[0]
		gene_set_des = f[1]
		gene_names = set(f[2:])
		new_gene_names = gene_names - set(genes)
		print (gene_set_id + '\t' + gene_set_des + '\t' + '\t'.join(new_gene_names), file=OUT)
	OUT.close()

def print_list(lst, size=5):
	'''
	Print lst to screen.
	
	parameters
	----------
	
	lst : list
		Input list.
	
	'''
	if len(lst) <= 10:
		print ('\t' + ','.join([str(i) for i in lst]))
	else:
		print ('\t' + ','.join([str(i) for i in lst[0:size]]) + ',...,' + ','.join([str(i) for i in lst[-size:]]))