#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

import pandas as pd

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','salary', 'bonus', 'long_term_incentive', 'deferred_income',
                 'deferral_payments', 'other', 'expenses','salary_bonus_ratio',
                 'total_payments', 'exercised_stock_options', 'restricted_stock', 'restricted_stock_deferred', 'total_stock_value',
                 'to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi','shared_receipt_with_poi'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
    data_dict.pop('TOTAL', 0)
    data_dict.pop("THE TRAVEL AGENCY IN THE PARK", 0 )
    data_dict.pop("LOCKHART EUGENE E", 0 )

dataDF = pd.DataFrame.from_dict(data_dict, orient = 'index' ,
                  dtype = float)
dataDF['salary_bonus_ratio'] = dataDF['bonus'] / dataDF['salary']
dataDF = dataDF.replace(['NaN','inf'], 0)
dataDF = dataDF[dataDF['restricted_stock_deferred'] <= 0]

data_dict = dataDF.to_dict(orient = 'index')

### Task 2: Remove outliers
### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
skb = SelectKBest(f_classif)
pca = PCA()
dtc = DecisionTreeClassifier(random_state = 100)

#pipeline = Pipeline(steps=[('Scaling',scaler),("PCA", pca), ("Tree", dtc)])
pipeline = Pipeline(steps=[("SKB",skb),("PCA", pca), ("Tree", dtc)])

params = {'SKB__k':range(3,10),'PCA__n_components':range(1,4),
          'Tree__min_samples_split': range(5,20),'Tree__criterion':['gini','entropy']}

split = StratifiedShuffleSplit(labels, test_size=0.3, random_state=42)

gs = GridSearchCV(pipeline, params, cv = split, scoring = 'f1')
    
gs.fit(features,labels)
clf=gs.best_estimator_
print clf

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)
