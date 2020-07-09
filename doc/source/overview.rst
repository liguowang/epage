About the package
------------------
The epage (Evaluate Protein Activity with Gene Expression) package contains several programs
to calculate the *composite expression score*, build and evaluate SVM model, and use SVM model
to predict new cases.

+--------------------+----------------------------------------------------------------------------------------+
| Name               | Description                                                                            |
+--------------------+----------------------------------------------------------------------------------------+
| gComposite.py      | Calculates these Composite Expression Scores                                           |
+--------------------+----------------------------------------------------------------------------------------+
| SVM_performance.py | Calculates these performance metrics of K-fold cross-validation                        |
+--------------------+----------------------------------------------------------------------------------------+
| SVM_predict.py     | Build SVM model from "train_file" and then predict cases in "data_file".               |
+--------------------+----------------------------------------------------------------------------------------+
| SVM_ROC.py         | Plot Receiver operating characteristic (ROC) curves using K-fold cross-validation.     |
+--------------------+----------------------------------------------------------------------------------------+

|

Workflow
--------
 1. We define the downstream target genes of a particular transcription factor.
 2. We collect the gene expression and mutation data. Use "Normal" and "Trundating" as training datasets.
 3. We run the **gComposite.py** to generate composite expression scores
 4. Run **SVM_performance.py** to check the performance of the SVM model, adjust training data and fine-tune the parameters. Usually, we need to run  *SVM_performance.py*  multiple times.
 5. Run **SVM_ROC.py** to generate ROC curve to visualize the performance.
 6. Run **SVM_predict.py** to predict new cases. 