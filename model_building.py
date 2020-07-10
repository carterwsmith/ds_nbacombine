#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 11:42:41 2020

@author: csmith
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.impute import SimpleImputer

df = pd.read_csv('combine_rookie_data_cleaned.csv')
df.columns

df_model_pre = df[['HEIGHT_W_SHOES', 'WINGSPAN', 'STANDING_REACH','THREE_QUARTER_SPRINT', 'STANDING_VERTICAL_LEAP', 'MAX_VERTICAL_LEAP', 'SPOT_FIFTEEN_TOP_KEY','SPOT_FIFTEEN_BREAK_RIGHT','SPOT_FIFTEEN_BREAK_LEFT','SPOT_NBA_TOP_KEY','SPOT_NBA_BREAK_RIGHT','SPOT_NBA_BREAK_LEFT','FG_PCT']]
 #imputation of NaN values with per column average
fill_NaN = SimpleImputer(missing_values=np.nan, strategy='mean')
fill_NaN = fill_NaN.fit(df_model_pre)
df_model = pd.DataFrame(fill_NaN.transform(df_model_pre))
df_model.columns = df_model_pre.columns

#test split training, testing for FG efficiency
from sklearn.model_selection import train_test_split, cross_val_score

X= df_model.drop('FG_PCT', axis=1)
y= df_model.FG_PCT.values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

#multiple linear regression
import statsmodels.api as sm
X_sm = X = sm.add_constant(X)
model = sm.OLS(y,X_sm)
model.fit()

from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(X_train, y_train)
lm_err = np.mean(cross_val_score(lm,X_train,y_train,scoring='neg_mean_absolute_error',cv=3))

#random forest regression
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()
rf_err = np.mean(cross_val_score(rf,X_train,y_train,scoring='neg_mean_absolute_error',cv=3))

#tune model with GridSearchCV
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}

gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_

#pickle model
import pickle
pickl = {'model': gs.best_estimator_}
pickle.dump( pickl, open( 'model_file' + ".p", "wb" ) )

file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']