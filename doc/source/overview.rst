overview
--------
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