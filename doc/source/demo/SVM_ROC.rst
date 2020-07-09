SVM_ROC.py
==============

Description
-----------

Plot Receiver operating characteristic (ROC) curves using K-fold cross-validation.


Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file=INPUT_FILE
                        Tab or space separated file. The first column contains
                        *sample IDs*; the second column contains *sample
                        labels* in integer (must be 0 or 1); the third column
                        contains *sample label names* (string, must be
                        consistent with column-2). The remaining columns
                        contain featuers used to build SVM model.
  -o OUT_FILE, --output=OUT_FILE
                        The prefix of the output file.
  -n N_FOLD, --nfold=N_FOLD
                        The original sample is randomly partitioned into *n*
                        equal sized subsamples (2 =< n <= 10). Of the n
                        subsamples, a single subsample is retained as the
                        validation data for testing the model, and the
                        remaining n − 1 subsamples are used as training data.
                        default=5.
  -C C_VALUE, --cvalue=C_VALUE
                        C value. default=1.0
  -s RAND_SEED, --seed=RAND_SEED
                        random_state seed used by the random number generator.
                        default=0
  -k S_KERNEL, --kernel=S_KERNEL
                        Specifies the kernel type to be used in the algorithm.
                        It must be one of ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’,
                        ‘precomputed’ or a callable. If none is given, ‘rbf’
                        will be used. default=linear
  --xl=X_LOW            The lower limit of X-axis (false positive rate).
                        default=-0.05
  --xu=X_UPPER          The upper limit of X-axis (false positive rate).
                        default=0.5
  --yl=Y_LOW            The lower limit of Y-axis (true positive rate).
                        default=0.5
  --yu=Y_UPPER          The upper limit of Y-axis (true positive rate).
                        default=1.05

                                                
Input files format
-------------------

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

 $ python3  SVM_ROC.py -i lung_CES_5features.tsv -o output_ROC -C 10                    


