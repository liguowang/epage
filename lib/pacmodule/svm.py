#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.utils import Bunch
from sklearn.model_selection import cross_val_score, cross_validate



def prep_data(infile):
	'''
	
	Description:
	------------
	Transform data matrix into Bunch object.
	
	Parameters
	----------
	infile : str
		Input file with its format specified below.
		
		* 1st-column : sample ID (string)
		* 2nd-column : binary label (intger, must be 0 or 1)
		* 3rd-column : label name (string, must be consistent with label)
		* 4th-column -  : featuers used to build SVM model
	
		The header row must exist.
	
	Example of input file
	--------------------
	sample_ID       Label   Label_name     feature_1      feature_2
	TCGA-A7-A0CE-11 0       Normal  57.29406049     38.16893788
	TCGA-A7-A0CH-11 0       Normal  55.26686259     37.11148777
	TCGA-A7-A0D9-01 1       Tumor  36.15425695     13.63843179
	TCGA-A7-A0DB-01 1       Tumor  38.71280272     45.02868304
	...
	
	Returns:
	--------
	A Bunch object.
	
	'''
	data = []
	target = []
	targetNames = {}
	target_names = []
	sample_names = []
	feature_names = []
	line_num = 0
	for l in open(infile,'r'):
		l = l.strip()
		if len(l) == 0:
			continue
		if l.startswith('#'):
			continue
		line_num += 1	  
  
		if line_num == 1:
			f = l.split()
			feature_names = f[3:]
		else:
			f = l.split()
			sample_names.append(f[0])
			target.append(int(f[1]))
			targetNames[int(f[1])] = f[2]
			data.append(list(map(float, f[3:])))
	uniq_target = sorted(targetNames.keys())
	
	target_names = [targetNames[i] for i in uniq_target]
	svm_data = Bunch(data = np.array(data), target = np.array(target), target_names = target_names, sample_names = sample_names, feature_names = feature_names)
	return (svm_data, targetNames)

def cal_scores(infile, k = 5, krnl = 'linear', nthreads = 5, C_value = 1.0):
	'''
	Description
	-----------
	Evaluate F1-micro, F1-macro and accuracy scores by cross-validation. The F1 score 
	can be interpreted as a weighted average of the precision and recall,
	where an F1 score reaches its best value at 1 and worst score at 0.
	
	The formula for the F1 score is:
		F1 = 2 * (precision * recall) / (precision + recall)
	
	F1-micro:
		Calculate metrics globally by counting the total true positives, false
		negatives and false positives.
	
	F1-macro:
		Calculate metrics for each label, and find their unweighted mean. This
		does not take label imbalance into account.	
	
	Parameters
	----------
	infile : str
		See above "prep_data" function for input file format.
	k : int
		integer, to specify the number of folds.
	krnl : string 
		Specifies the kernel type to be used in the algorithm. It must be one of ‘linear’,
		‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’ or a callable. If none is given, ‘rbf’ will
		be used.
			
	Returns
	-------
	F1 macro scores and F1 micro scores.
	
	'''
	print ("Preprocessing data ...", file = sys.stderr)
	(a, b) = prep_data(infile)
	
	# cross validaetion
	clf = svm.SVC(kernel = krnl, C=C_value, gamma='auto',probability=True)
	
	
	print('Evaluate metric(s) by cross-validation ...',file=sys.stderr)
	scores = cross_validate(clf, a.data, a.target, cv=k, n_jobs = nthreads, scoring=['f1_macro','f1_micro', 'accuracy','precision','recall'])
	
	print ("F1 score is the weighted average of the precision and recall. F1 = 2 * (precision * recall) / (precision + recall)")
	print ('\n')
	print ("F1_macro calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.")
	for i in range(len(scores['test_f1_macro'])):
		print ("\tIteration %d: %f" % (i+1, scores['test_f1_macro'][i]))
	print("F1-macro: %0.4f (+/- %0.4f)" % (scores['test_f1_macro'].mean(), scores['test_f1_macro'].std() * 2))				   
	print ('\n')
	
	print ("F1_micro calculate metrics globally by counting the total true positives, false negatives and false positives.")
	for i in range(len(scores['test_f1_micro'])):
		print ("\tIteration %d: %f" % (i+1, scores['test_f1_micro'][i]))
	print("F1-micro: %0.4f (+/- %0.4f)" % (scores['test_f1_micro'].mean(), scores['test_f1_micro'].std() * 2))				   
	print ('\n')
	
	print ("accuracy is equal to F1_micro for binary classification problem")
	for i in range(len(scores['test_accuracy'])):
		print ("\tIteration %d: %f" % (i+1, scores['test_accuracy'][i]))
	print("Accuracy: %0.4f (+/- %0.4f)" % (scores['test_accuracy'].mean(), scores['test_accuracy'].std() * 2))		
	print ('\n')		   
	
	print ('Precision = tp / (tp + fp). It measures "out of all *predictive positives*, how many are correctly predicted?"')
	for i in range(len(scores['test_precision'])):
		print ("\tIteration %d: %f" % (i+1, scores['test_precision'][i]))
	print("Precision: %0.4f (+/- %0.4f)" % (scores['test_precision'].mean(), scores['test_precision'].std() * 2))		
	print ('\n')	
	
	print ('Recall = tp / (tp + fn). Recall (i.e. sensitivity) measures "out of all  *positives*, how many are correctly predicted?"')
	for i in range(len(scores['test_recall'])):
		print ("\tIteration %d: %f" % (i+1, scores['test_recall'][i]))
	print("Recall: %0.4f (+/- %0.4f)" % (scores['test_recall'].mean(), scores['test_recall'].std() * 2))		
	print ('\n')
	
	return (scores)
	

	"""
	print ("Cross validation using f1 macro scoring ...", file = sys.stderr)
	f1_macro_scores = cross_val_score(clf, a.data, a.target, cv=k, scoring='f1_macro',n_jobs = nthreads)
	for i in range(len(f1_macro_scores)):
		print ("Iteration %d: %f" % (i+1, f1_macro_scores[i]), file=sys.stderr)
	print("F1-macro: %0.4f (+/- %0.2f)" % (f1_macro_scores.mean(), f1_macro_scores.std() * 2))				   

	print ("Cross validation using f1 micro scoring ...", file = sys.stderr)
	f1_micro_scores = cross_val_score(clf, a.data, a.target, cv=k, scoring='f1_micro',n_jobs = nthreads)
	for i in range(len(f1_micro_scores)):
		print ("Iteration %d: %f" % (i+1, f1_micro_scores[i]), file=sys.stderr)
	print("F1-micro: %0.4f (+/- %0.2f)" % (f1_micro_scores.mean(), f1_micro_scores.std() * 2))				   

	print ("Estimate accuracy ...", file = sys.stderr)
	acc_scores = cross_val_score(clf, a.data, a.target, cv=k, scoring='accuracy',n_jobs = nthreads)
	for i in range(len(acc_scores)):
		print ("Iteration %d: %f" % (i+1, acc_scores[i]), file=sys.stderr)
	print("Accuracy: %0.4f (+/- %0.2f)" % (acc_scores.mean(), acc_scores.std() * 2))				  
	return(f1_macro_scores, f1_micro_scores, acc_scores)
	"""				   

def plot_sROC(infile, test_size = 0.4, seed = 0, shuf = True, outfile = 'ROC'):
	'''
	Description
	-----------
	Plot a single Receiver operating characteristic (ROC) curve.
	
	Parameters
	----------
	infile : str
		See above "prep_data" function for input file format.
	
	test_size : float or int
		If float, should be between 0.0 and 1.0 and represent the proportion of
		the dataset to include in he test split. If int, represents the
		absolute number of test samples.
	
	seed : int
		random_state seed used by the random number generator.
		
	shuf : bool
		Whether or not to shuffle the data before splitting
	
	outfile : str
		prefix of output files. 
	
	'''
	from sklearn.metrics import roc_curve, auc
	#from sklearn.preprocessing import label_binarize
	import matplotlib.pyplot as plt

	print ("Preprocessing data ...", file = sys.stderr)
	(a, b) = prep_data(infile)
	
	X = a.data
	y = a.target
	# Binarize the output
	#y = label_binarize(y, classes=[0, 1])
		
	randomState = np.random.RandomState(seed)

	# shuffle and split training and test sets
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size, random_state = randomState, shuffle = shuf)

	# Learn to predict each class against the other
	classifier = svm.SVC(kernel='linear', probability=True, random_state = randomState)
	y_score = classifier.fit(X_train, y_train).decision_function(X_test)
		
	# Compute ROC curve and ROC area for each class
	fpr = []
	tpr = []
	roc_auc = []
	fpr, tpr, thresholds = roc_curve(y_test, y_score,pos_label=1)
	roc_auc = auc(fpr, tpr)
	
	
	print ("FPR\tTPR\tThreshold")
	for i,j,t in zip(fpr,tpr, thresholds):
		print (str(i) + '\t' + str(j) + '\t' + str(t))
	
	print ("AUC is : %f" % roc_auc)
	
	plt.figure()
	plt.plot(fpr, tpr, color='magenta',lw=1)
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('ROC curve (AUC = %0.3f)' % roc_auc)
	plt.savefig('%s.pdf' % outfile, bbox_inches='tight')
	plt.show()


def plot_cvROC(infile, outfile, xl, xu, yl, yu, krnl, k = 5, C_value = 1.0, seed = 0):
	'''
	Description
	-----------
	Plot Receiver operating characteristic (ROC) curves using cross-validation.
	
	Parameters
	----------
	infile : str
		See above "prep_data" function for input file format.
	
	k : int
		integer, to specify the number of folds
	
	seed : int
		random_state seed used by the random number generator.
	
	outfile : str
		prefix of output files. 
	
	krnl : string 
		Specifies the kernel type to be used in the algorithm. It must be one of ‘linear’,
		‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’ or a callable. If none is given, ‘rbf’ will
		be used.
	'''
	from sklearn.metrics import roc_curve, auc
	from scipy import interp
	from sklearn.model_selection import StratifiedKFold
	import matplotlib.pyplot as plt

	print ("Preprocessing data ...", file = sys.stderr)
	(a, b) = prep_data(infile)
	
	X = a.data
	n_samples, n_features = X.shape
	y = a.target
	
	randomState = np.random.RandomState(seed)
	cv = StratifiedKFold(n_splits = k)
	classifier = svm.SVC(kernel = krnl, C = C_value, probability=True, random_state=randomState)	
	
	tprs = []
	aucs = []
	mean_fpr = np.linspace(0, 1, 100)
	
	i = 0
	for train, test in cv.split(X, y):
		probas_ = classifier.fit(X[train], y[train]).predict_proba(X[test])
		# Compute ROC curve and area the curve
		fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
		tprs.append(interp(mean_fpr, fpr, tpr))
		tprs[-1][0] = 0.0
		roc_auc = auc(fpr, tpr)
		aucs.append(roc_auc)
		plt.plot(fpr, tpr, lw=1, alpha=0.3, label='ROC fold %d (AUC = %0.4f)' % (i, roc_auc))
		i += 1
	plt.plot([0, 1], [0, 1], linestyle='--', lw=1, color='blue', label='Chance', alpha=.8)

	mean_tpr = np.mean(tprs, axis=0)
	mean_tpr[-1] = 1.0
	mean_auc = auc(mean_fpr, mean_tpr)
	std_auc = np.std(aucs)
	plt.plot(mean_fpr, mean_tpr, color='magenta',label=r'Mean ROC (AUC = %0.4f $\pm$ %0.4f)' % (mean_auc, std_auc),lw=1, alpha=1)

	std_tpr = np.std(tprs, axis=0)
	tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
	tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
	plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,label=r'$\pm$ 1 std. dev.')

	plt.xlim([xl, xu])
	plt.ylim([yl, yu])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('ROC curve')
	plt.legend(loc="lower right")
	plt.savefig('%s.pdf' % outfile, bbox_inches='tight')
	plt.show()
	
		
def svm_predict(train_file, data_file, krnl = 'linear', C_value = 1.0, mname = 'SVM_model.sav'):
	'''

	Description
	-----------
	Build SVM model from data in 'train_file' and predict data in 'data_file'.
	
	Parameters
	----------
	
	train_file : str
		File containing  data for training. See above "prep_data" function for file
		format.
	
	data_file : str
		File containing data for prediction. See above "prep_data" function for file
		format.
	
	mname : str
		Name of file containg SVM model
	'''
	print ("Preprocessing data ...", file = sys.stderr)
	(a, labels) = prep_data(train_file)
	
	# fit model
	print ("Building SVM model ...", file = sys.stderr)
	clf = svm.SVC(kernel=krnl, C=C_value).fit(a.data, a.target)
	
	# save model to file
	pickle.dump(clf, open(mname, 'wb'))
	
	# open model
	#loaded_model = pickle.load(open(mname, 'rb'))
	
	
	print ("Predicting ...", file = sys.stderr)
	#print ("\nsample_ID\tPredicted_label\tPredicted_name")
	for l in open(data_file,'r'):
		l = l.strip()
		if len(l) == 0:continue
		if l.startswith('#'):continue
		if l.startswith('TCGA_ID'):
			print ('\t'.join(["TCGA_ID", "Ori_Label", "Ori_name", "Predict_Label", "Predict_Name"]))
			continue
		f = l.split()
		sample_name = f[0]
		ori_label = f[1]
		ori_name = f[2]
		feature_values = f[3:]
		predict_lab = clf.predict([feature_values])[0]
		if predict_lab in labels:
			predict_name = labels[predict_lab]
		else:
			predict_name = "unknown"
		
		print ("%s\t%s\t%s\t%d\t%s" % (sample_name, ori_label, ori_name,predict_lab, predict_name))
	
			
if __name__=='__main__':
	  cal_scores(sys.argv[1])
	  #svm_predict(sys.argv[1], sys.argv[2])
	  #plot_sROC(sys.argv[1])
	  #plot_cvROC(sys.argv[1])
