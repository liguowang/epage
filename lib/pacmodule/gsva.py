#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 11:41:17 2019

Calculate ssGSEA, GSVA, zscore, and plage. 
Must install Bioconductor package: GSVA and GSEAbase

@author: m102324
"""
import os,sys
import subprocess

def run_gsva(routfile, gmtfile, expr_file,outfile,n_proc):
	
	ROUT = open(routfile,'w')
	geneSetNames = []
	for l in open(gmtfile):
		l = l.strip()
		if l.startswith('#'):continue
		f = l.split('\t')
		# must has at least one gene
		if len(f) < 3: continue
		geneSetNames.append(f[0])
		
	# set work dir	
	curr_dir = os.getcwd()
	print ('setwd("%s")' % curr_dir, file=ROUT)
	
	#check required packages
	print ('if(!require(%s)){install.packages("%s");library(%s)}' % ("GSEABase", "GSEABase","GSEABase"), file=ROUT)	
	print ('if(!require(%s)){install.packages("%s");library(%s)}' % ("GSVA", "GSVA","GSVA"), file=ROUT)	
	print ('\n', file=ROUT)
	# load GMT and expr files
	print ('geneSets = getGmt("%s")' % gmtfile, file=ROUT)
	print ('mat = as.matrix(read.csv("%s", sep="\\t",header=TRUE,row.names=1,check.names=FALSE))' % expr_file, file=ROUT)
	print ('\n', file=ROUT)
	
	# calculate scores
	print ("output_gsva = gsva(mat, geneSets, method='gsva', kcdf='Gaussian', parallel.sz=%d)" % n_proc, file=ROUT)
	print ("output_ssgsea = gsva(mat, geneSets, method='ssgsea', kcdf='Gaussian', parallel.sz=%d, ssgsea.norm=TRUE)" % n_proc, file=ROUT)
	print ("output_zscore = gsva(mat, geneSets, method='zscore', kcdf='Gaussian', parallel.sz=%d)" % n_proc, file=ROUT)
	print ("output_plage = gsva(mat, geneSets, method='plage', kcdf='Gaussian', parallel.sz=%d)" % n_proc, file=ROUT)
	print ('\n', file=ROUT)
	
	# update row names
	print ("row.names(output_gsva) <- c(%s)" % (','.join(["'" + 'gsva_' + i  + "'" for i in geneSetNames])), file=ROUT)
	print ("row.names(output_ssgsea) <- c(%s)" % (','.join(["'" + 'ssGSEA_' + i  + "'" for i in geneSetNames])), file=ROUT)
	print ("row.names(output_zscore) <- c(%s)" % (','.join(["'" + 'zscore_' + i  + "'" for i in geneSetNames])), file=ROUT)
	print ("row.names(output_plage) <- c(%s)" % (','.join(["'" + 'plage_' + i  + "'" for i in geneSetNames])), file=ROUT)
	print ('\n', file=ROUT)
	
	# write to file
	print ("write.csv(t(output_gsva),   '%s',quote=F)" % (outfile + '_gsva.csv'), file=ROUT)
	print ("write.csv(t(output_ssgsea),   '%s',quote=F)" % (outfile + '_ssgsea.csv'), file=ROUT)
	print ("write.csv(t(output_zscore),   '%s',quote=F)" % (outfile + '_zscore.csv'), file=ROUT)
	print ("write.csv(t(output_plage),   '%s',quote=F)" % (outfile + '_plage.csv'), file=ROUT)
	
	ROUT.close()
	try:
		subprocess.call("Rscript " + routfile, shell=True)
	except:
		print ("Cannot run '%s', please make sure R packages '%s' and '%s' are properly installed" % (routfile, "GSEABase", "GSVA"), file=sys.stderr )
		sys.exit()
