# import libraries
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

# read in dataframe
weather_aus = pd.read_csv(f'{dir_path}\weatherAUS.csv')
weather_aus = weather_aus.dropna() # drop all rows with NA values
weather_aus.drop(['Date'], axis=1, inplace=True)
weather_aus.drop(['Location'], axis=1, inplace=True)

# one hot encoding
df = pd.get_dummies(data=weather_aus, columns=['WindGustDir','WindDir9am','WindDir3pm'])
df['RainToday'] = df['RainToday'].astype(str)
df['RainTomorrow'] = df['RainTomorrow'].astype(str)
lb = preprocessing.LabelBinarizer()

df['RainToday'] = lb.fit_transform(df['RainToday'])
df['RainTomorrow'] = lb.fit_transform(df['RainTomorrow'])

y = df['RainTomorrow']
X = df.drop(['RainTomorrow'], axis=1) # drop target from dataframe

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

pipe = Pipeline([('scaler', StandardScaler()), ('LR', LogisticRegression(max_iter=100000))])

# initiate the model
pipe.fit(X_train, y_train)
score = pipe.score(X_train, y_train)

# model accuracies
ns_probs = [0 for _ in range(len(y_test))]
lr_probs = pipe.predict_proba(X_test)
lr_probs = lr_probs[:, 1]

ns_auc = roc_auc_score(y_test, ns_probs)
lr_auc = roc_auc_score(y_test, lr_probs)

print('Accuracy Score:%.3f' % (score))
print('No Skill: ROC AUC=%.3f' % (ns_auc))
print('RFC: ROC AUC=%.3f' % (lr_auc))

