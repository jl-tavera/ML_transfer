'''
LIBRARIES
'''

import FBrefScraper as FBref
import DataFunctions as Dfx
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import export_graphviz
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

import pydot



'''
https://towardsdatascience.com/random-forest-in-python-24d0893d51c0
'''

ML_df = FBref.loadCleanCSV('ML_df.csv')

features= ML_df.drop(['group_min', 'Name', 'Unnamed: 0', 'min_norm'], axis = 1)
features = features.reset_index()
features = pd.get_dummies(features)
feature_list = list(features.columns)
features = np.array(features)

labels = np.array(ML_df['group_min'])

train_features, test_features, train_labels, test_labels = train_test_split(features,
                                                                labels,
                                                                 test_size = 0.25,
                                                                  random_state = 42)

rf = RandomForestClassifier(n_estimators = 1000, random_state = 42)
# Train the model on training data
rf.fit(train_features, train_labels);

# Use the forest's predict method on the test data
predictions = rf.predict(test_features)
# Calculate the absolute errors
errors = abs(predictions - test_labels)
# Print out the mean absolute error (mae)
print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')
# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / test_labels)
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')



cm = confusion_matrix(test_labels,predictions )
print(cm)

plot = plt.figure(figsize=(10,7))
plot = sn.heatmap(cm, annot=True)
plt.xlabel('Predicted')
plt.ylabel('Truth')
plot = plot.get_figure()
path = 'img/cm'
plot.savefig( path, dpi=300)

# Get numerical feature importances
importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances 
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];


