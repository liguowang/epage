SVM_performance.py
===================

Description
-----------

Calculating performance metrics using K-fold cross-validation.

 * F1_micro
 * F1_macro
 * Accuracy
 * Precision
 * Recall
 

Options
----------
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file=INPUT_FILE
                        Tab or space separated file. The first column contains
                        *sample IDs*; the second column contains *sample
                        labels* in integer (must be 0 or 1); the third column
                        contains *sample label names* (string, must be
                        consistent with column-2). The remaining columns
                        contain featuers used to build SVM model.
  -n N_FOLD, --nfold=N_FOLD
                        The original sample is randomly partitioned into *n*
                        equal sized subsamples (2 =< n <= 10). Of the n
                        subsamples, a single subsample is retained as the
                        validation data for testing the model, and the
                        remaining n − 1 subsamples are used as training data.
                        default=5.
  -p N_THREAD, --nthread=N_THREAD
                        Number of threads to use. default=2
  -C C_VALUE, --cvalue=C_VALUE
                        C value. default=1.0
  -k S_KERNEL, --kernel=S_KERNEL
                        Specifies the kernel type to be used in the algorithm.
                        It must be one of ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’,
                        ‘precomputed’ or a callable. If none is given, ‘rbf’
                        will be used. default=linear

Input files format
------------------------

+----------+-------+------------+-----------+-----------+-----------+---+-----------+
| ID       | Label | Label_name | feature_1 | feature_2 | feature_3 | … | feature_n |
+----------+-------+------------+-----------+-----------+-----------+---+-----------+
| sample_1 | 1     | WT         | 1560      | 795       | 0.9716    | … | feature_n |
+----------+-------+------------+-----------+-----------+-----------+---+-----------+
| sample_2 | 1     | WT         | 784       | 219       | 0.4087    | … | feature_n |
+----------+-------+------------+-----------+-----------+-----------+---+-----------+
| sample_3 | 1     | WT         | 2661      | 2268      | 1.1691    | … | feature_n |
+----------+-------+------------+-----------+-----------+-----------+---+-----------+
| sample_4 | 0     | Mut        | 643       | 198       | 0.5458    | … | feature_n |
+----------+-------+------------+-----------+-----------+-----------+---+-----------+
| sample_5 | 0     | Mut        | 534       | 87        | 1.0545    | … | feature_n |
+----------+-------+------------+-----------+-----------+-----------+---+-----------+
| sample_6 | 0     | Mut        | 332       | 75        | 0.5115    | … | feature_n |
+----------+-------+------------+-----------+-----------+-----------+---+-----------+


Command
---------

::

 $  python3  gComposite.py  -e lung_expr.81genes.tsv -g  lung_p53_target.gmt  -k lung_group.csv -o lung                        

Output files
------------
 * output.R : R script to run GSVA package
 * output.mat.tsv : Data that is actually used. Might be the same as the input "lung_expr.81genes.tsv", or just a subset of "lung_expr.81genes.tsv". 
 * output_combined.csv : comma-separated composite expression score (group IDs were included)
 * output_combined.tsv : TAB-separated composite expression score (group IDs were NOT included)
 * output_gsva.csv : GSVA scores
 * output_pca.csv : First two principal components of PCA. 
 * output_plage.csv : PLAGE scores
 * output_ssgsea.csv : ssGSEA scores
 * output_zscore.csv : Z-scores

The file "output_combined.csv" contains everything!


