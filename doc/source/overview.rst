Overview
=========

gComposite.py
-------------
This program Calculates these Composite Expression Scores.
 * Gene Set Variation Analysis (GSVA). [1]_
 * Single Sample GSEA (ssGSEA). [2]_
 * zscore [3]_
 * plage [4]_
 
SVM_performance.py
------------------
This program calculates these performance metrics of K-fold cross-validation.
 * F1_micro
 * F1_macro
 * Accuracy
 * Precision
 * Recall

SVM_predict.py
--------------
Build SVM model from "train_file" and then predict cases in "data_file".
 
SVM_ROC.py
---------- 
Plot `Receiver operating characteristic (ROC) <https://en.wikipedia.org/wiki/Receiver_operating_characteristic>`_ curves using K-fold cross-validation.
 
 
References
----------

.. [1] Hänzelmann S, Castelo R, Guinney J. GSVA: gene set variation analysis for microarray and RNA-seq data. BMC Bioinformatics. 2013;14:7. Published 2013 Jan 16. doi:10.1186/1471-2105-14-7
.. [2] Barbie DA, Tamayo P, Boehm JS, et al. Systematic RNA interference reveals that oncogenic KRAS-driven cancers require TBK1. Nature. 2009;462(7269):108-112. doi:10.1038/nature08460
.. [3] Lee E, Chuang HY, Kim JW, Ideker T, Lee D. Inferring pathway activity toward precise disease classification. PLoS Comput Biol. 2008;4(11):e1000217. doi:10.1371/journal.pcbi.1000217
.. [4] Tomfohr J, Lu J, Kepler TB. Pathway level analysis of gene expression using singular value decomposition. BMC Bioinformatics. 2005;6:225. Published 2005 Sep 12. doi:10.1186/1471-2105-6-225