SVM_predict.py
==============

Description
-----------

Build SVM model from "train_file" and then predict cases in "data_file"


Options
----------
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -t TRAIN_FILE, --train_file=TRAIN_FILE
                        Tab or space separated file (for tranining purpose, to
                        build SVM model). The first column contains *sample
                        IDs*; the second column contains *sample labels* in
                        integer (must be 0 or 1); the third column contains
                        *sample label names* (string, must be consistent with
                        column-2). The remaining columns contain featuers used
                        to build SVM model.
  -d DATA_FILE, --data_file=DATA_FILE
                        Tab or space separated file (new data to predict the
                        label). The first column contains *sample IDs*; the
                        second column contains *sample labels* in integer
                        (must be 0 or 1); the third column contains *sample
                        label names* (string, must be consistent with
                        column-2). The remaining columns contain featuers used
                        to build SVM model.
  -C C_VALUE, --cvalue=C_VALUE
                        C value. default=1.0
  -k S_KERNEL, --kernel=S_KERNEL
                        Specifies the kernel type to be used in the algorithm.
                        It must be one of ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’,
                        ‘precomputed’ or a callable. If none is given, ‘rbf’
                        will be used. default=linear
                        
Input files format
-------------------
TRAIN_FILE and DATA_FILE use the same format as below. the 2nd and 3rd columns in DATA_FILE
can be consideres as **Original Label** and **Original Name**. 

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

 $ python3  SVM_predict.py -t lung_CES_5features.tsv  -d lung_CES_data_to_predict.tsv -C 10                    

Output to screen
-----------------

::

 TCGA_ID	Ori_Label	Ori_name	Predict_Label	Predict_Name
 TCGA-05-4244	unknown	TP53_WT	1	Truncating
 TCGA-05-4249	unknown	TP53_WT	1	Truncating
 TCGA-05-4250	unknown	TP53_WT	1	Truncating
 TCGA-05-4389	unknown	TP53_WT	1	Truncating
 TCGA-05-4390	unknown	TP53_WT	1	Truncating
 TCGA-05-4403	unknown	TP53_WT	1	Truncating
 TCGA-38-7271	unknown	TP53_WT	1	Truncating
 TCGA-38-A44F	unknown	TP53_WT	0	Normal
 TCGA-39-5030	unknown	TP53_WT	1	Truncating
