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

Example of input file
---------------------

::

 $ cat lung_CES_5features.tsv
 TCGA_ID Label   Group   gsva_p53_activated      gsva_p53_repressed      ssGSEA_p53_activated    ssGSEA_p53_repressed    PC1
 TCGA-22-4593-11A        0       Normal  0.97337963      -0.965872505    0.446594884     -0.332230329    10.12036762
 TCGA-22-4609-11A        0       Normal  0.974507532     -0.971830001    0.480743696     -0.373937866    12.57932272
 TCGA-22-5471-11A        0       Normal  0.981934732     -0.991054313    0.465087717     -0.354705367    11.50908022
 TCGA-22-5472-11A        0       Normal  0.914660832     -0.889643616    0.433541263     -0.316566781    7.96785884
 TCGA-22-5478-11A        0       Normal  0.983080513     -0.989789407    0.478239013     -0.370840097    11.81998124
 TCGA-22-5481-11A        0       Normal  0.958950969     -0.973021839    0.441116626     -0.325822867    10.62201083
 TCGA-22-5482-11A        0       Normal  0.97113164      -0.976324136    0.471515295     -0.362373723    10.78576876
 TCGA-22-5483-11A        0       Normal  0.957377049     -0.986013986    0.378674475     -0.253223408    7.487083257
 TCGA-22-5489-11A        0       Normal  0.963911525     -0.982725528    0.45219094      -0.339061168    9.49806089
 TCGA-22-5491-11A        0       Normal  0.981934732     -0.991054313    0.475345705     -0.367218333    12.2813137
 TCGA-33-4587-11A        0       Normal  0.90739615      -0.930774072    0.403446401     -0.281428331    9.368460346
 TCGA-33-6737-11A        0       Normal  0.962025316     -0.957522049    0.495340808     -0.391557543    10.79155095
 TCGA-34-7107-11A        0       Normal  0.949717514     -0.934120795    0.451010344     -0.337452999    10.04177079
 TCGA-34-8454-11A        0       Normal  0.992397661     -0.987269255    0.480060883     -0.372603029    10.6050578
 ...

Command
---------

::

 $  python3  SVM_performance.py -i lung_CES_5features.tsv -C 10                       

.. note::
   There is no rule of thumb to choose a C value, people can try a bunch of different C values
   and choose the one which gives you "best performance scores"
   
Output to screen
-----------------

::

 Preprocessing data ...
 Evaluate metric(s) by cross-validation ...
 F1 score is the weighted average of the precision and recall. F1 = 2 * (precision * recall) / (precision + recall)

 
 F1_macro calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.
 	Iteration 1: 1.000000
 	Iteration 2: 0.983518
 	Iteration 3: 1.000000
 	Iteration 4: 1.000000
 	Iteration 5: 0.967273
 F1-macro: 0.9902 (+/- 0.0262)
 
 
 F1_micro calculate metrics globally by counting the total true positives, false negatives and false positives.
 	Iteration 1: 1.000000
 	Iteration 2: 0.986301
 	Iteration 3: 1.000000
 	Iteration 4: 1.000000
 	Iteration 5: 0.972222
 F1-micro: 0.9917 (+/- 0.0222)
 
 
 accuracy is equal to F1_micro for binary classification problem
 	Iteration 1: 1.000000
 	Iteration 2: 0.986301
 	Iteration 3: 1.000000
 	Iteration 4: 1.000000
 	Iteration 5: 0.972222
 Accuracy: 0.9917 (+/- 0.0222)
 
 
 Precision = tp / (tp + fp). It measures "out of all *predictive positives*, how many are correctly predicted?"
 	Iteration 1: 1.000000
 	Iteration 2: 1.000000
 	Iteration 3: 1.000000
 	Iteration 4: 1.000000
 	Iteration 5: 1.000000
 Precision: 1.0000 (+/- 0.0000)
 
 
 Recall = tp / (tp + fn). Recall (i.e. sensitivity) measures "out of all  *positives*, how many are correctly predicted?"
 	Iteration 1: 1.000000
 	Iteration 2: 0.980769
 	Iteration 3: 1.000000
 	Iteration 4: 1.000000
 	Iteration 5: 0.960784
 Recall: 0.9883 (+/- 0.0313)