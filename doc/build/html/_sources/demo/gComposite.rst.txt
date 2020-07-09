gComposite.py
==============

Description
-----------

This program Calculates these Composite Expression Scores. Compared to expression score of a single gene,
*composite expression score* measure the overall activity of **a set of genes**. It is often used
to measure the activity of a pathway or transcription factor.

It calculates these scores:

 * Gene Set Variation Analysis (GSVA). [1]_
 * Single Sample GSEA (ssGSEA). [2]_
 * zscore [3]_
 * plage [4]_
 

.. note::
   The R package `GSVA <https://bioconductor.org/packages/release/bioc/html/GSVA.html>`_ will be automatically installed
   and used to calculate these scores.

Options
----------
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -e EXPR_FILE, --expr_matrix=EXPR_FILE
                        Tab-separated data matrix file containing gene
                        expression values. The 1st row containing
                        sample/patient IDs and the 1st column containing gene
                        symbols(mut be unique). File can be compressed (.gz,
                        .Z, .z, .bz, .bz2, bzip2).
  -g GENE_FILE, --gene=GENE_FILE
                        GMT file. The GMT file format is a tab delimited file
                        format that describes gene sets (Each gene set is
                        described by a name, a description, and the genes in
                        the gene set). In the GMT format, each row represents
                        a gene set. The first column is get set name (must be
                        unique). The second column is brief description (can
                        be 'na').
  -k GROUP_FILE, --group=GROUP_FILE
                        Group file (in CSV format). First column is sample ID,
                        second column is group ID
  -s SAMPLE_FILE, --sample=SAMPLE_FILE
                        Sample list file containing sample IDs. Each row can
                        be a single sample ID, a comma-separated sample IDs or
                        a space-separated sample IDs. Sample IDs must match
                        exactly to those in the data matrix file. If omitted,
                        calculated activity scores for *all* the samples. File
                        can be compressed (.gz, .Z, .z, .bz, .bz2, bzip2).
                        default=none (All samples will be used)
  -l, --log             If True, will do log2(x+1) transformation for gene
                        experssion values. Must set to 'True' if expressin
                        values are RNA-seq count. default=False
  -p N_THREAD, --processor=N_THREAD
                        Number of processors to use when doing the
                        calculations in parallel. default=0 (use all available
                        processors)
  -o OUT_FILE, --output=OUT_FILE
                        The prefix of the output file.



Input files (examples)
------------------------

- Gene expression table. Example: lung_expr.81genes.tsv 
- Gene list in GMT format. Example: lung_p53_target.gmt 
- Group file. Example: lung_group.csv

Command
---------

::

 $  python3  gComposite.py  -e lung_expr.81genes.tsv -g  lung_p53_target.gmt  -k lung_group.csv -o lung                        

Output files
------------
 * output.R : R script to run GSVA package
 * output.mat.tsv : Data that is actually used. Might be the same as the input "lung_expr.81genes.tsv", or just a subset of "lung_expr.81genes.tsv". 
 * output_combined.tsv : comma-separated composite expression score (group IDs were also included)
 * output_gsva.csv : GSVA scores
 * output_pca.csv : First two principal components of PCA. 
 * output_plage.csv : PLAGE scores
 * output_ssgsea.csv : ssGSEA scores
 * output_zscore.csv : Z-scores

.. note::
   The file "output_combined.tsv" contains everything you need for SVM model building and testing.

References
----------

.. [1] Hänzelmann S, Castelo R, Guinney J. GSVA: gene set variation analysis for microarray and RNA-seq data. BMC Bioinformatics. 2013;14:7. Published 2013 Jan 16. doi:10.1186/1471-2105-14-7
.. [2] Barbie DA, Tamayo P, Boehm JS, et al. Systematic RNA interference reveals that oncogenic KRAS-driven cancers require TBK1. Nature. 2009;462(7269):108-112. doi:10.1038/nature08460
.. [3] Lee E, Chuang HY, Kim JW, Ideker T, Lee D. Inferring pathway activity toward precise disease classification. PLoS Comput Biol. 2008;4(11):e1000217. doi:10.1371/journal.pcbi.1000217
.. [4] Tomfohr J, Lu J, Kepler TB. Pathway level analysis of gene expression using singular value decomposition. BMC Bioinformatics. 2005;6:225. Published 2005 Sep 12. doi:10.1186/1471-2105-6-225


