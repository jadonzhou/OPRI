import pandas as pd
import numpy as np
import pandas as pd
from pandas import DataFrame
import datetime as dt
import re
import csv
from sklearn.linear_model import LinearRegression,LogisticRegression,Ridge,RidgeCV,Lasso, LassoCV
from sklearn.model_selection import train_test_split,GridSearchCV,cross_val_score,cross_validate
from sklearn import  metrics as mt
from  statsmodels.stats.outliers_influence import variance_inflation_factor
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from decimal import *
from collections import Counter
import math
from scipy import stats
from scipy.stats.mstats import kruskalwallis
from pandas import read_csv
import os
from datetime import datetime
from calendar import isleap
import datetime
import time

Path="/Volumes/T7/OPRI UK/Objective 9/"
file="COPD general 6 new"
marker="events"
database = pd.read_csv(Path+file+".csv")
database['Reference Key']=database['patid']
database['Reference Date']=database['idx_dte']
#database['Baseline Date'] = pd.to_datetime(database['Baseline Date'])
comCategory = pd.read_csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/Tools/Comorbidity/ICD10Codes.csv", encoding='windows-1252')
#comCategory = comCategory.iloc[:,0:2]
#comCategory = pd.read_csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/Tools/Comorbidity/HA Prior Comorbidities.csv", encoding='windows-1252')
comCategory=comCategory.astype(str)
comCategorys=pd.concat(comCategory.iloc[:,i] for i in range(comCategory.shape[1])).tolist()
Dx = pd.read_csv("/Volumes/T7/OPRI UK/Objective 9/cprd_cardio_long_table with read code.csv")
Dx = Dx.apply(lambda col: pd.to_datetime(col, errors='ignore') 
              if col.dtypes == object 
              else col, 
              axis=0)
Dx=Dx[Dx['patid'].isin(database['patid'].tolist())]
Dx=Dx[Dx['idx_dte']!='2012-06-']
Dx=Dx[Dx['idx_dte']!='2015-09-']
Dx=Dx[Dx['idx_dte']!='1/0/1900']
Dx['idx_dte'] = pd.to_datetime(Dx['idx_dte'])
Dx=Dx[Dx['ICD_PRIMARY'].isin(comCategorys)]
Dx['idx_dte'] = pd.to_datetime(Dx['idx_dte'])
Dx = Dx.sort_values(by = 'idx_dte',ascending=True)
#result_age=pd.DataFrame(np.zeros((databas ane.shape[0],comCategory.shape[1])))
#result_age.columns=comCategory.columns
result_disease=pd.DataFrame(np.zeros((database.shape[0],comCategory.shape[1])))
result_disease.columns=comCategory.columns
result_date=pd.DataFrame(np.zeros((database.shape[0],comCategory.shape[1])))
result_date.columns=comCategory.columns
for p in range(database.shape[0]):
    print(p)
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    comorbidities=Dx[(Dx['Reference Key']==database.iloc[p,0]) | (Dx['Reference Key']==str(database.iloc[p,0]))]
    comorbidities=comorbidities.sort_values(by = 'Reference Date',ascending=True)
    baselineDate=database.iloc[p,1]
    #comorbidities = comorbidities[(comorbidities['Reference Date']>=pd.to_datetime(baselineDate))]
    for i in range(comorbidities.shape[0]):
        code=comorbidities.iloc[i,7]
        for j in range(comCategory.shape[1]):
            if code in comCategory.iloc[:,j].dropna().tolist() or str(code) in comCategory.iloc[:,j].dropna().tolist():
                result_disease.iloc[p,j]=comorbidities.shape[0]
                #result_disease.iloc[p,j]=1
                #result_age.iloc[p,j]=comorbidities.iloc[i,8]
                result_date.iloc[p,j]=",".join([x.strftime('%Y/%m/%d') for x in comorbidities['Reference Date']])
                #result_date.iloc[p,j]=comorbidities.iloc[i,3].strftime('%Y/%m/%d')
                #difference=datetime.strptime(comorbidities.iloc[i,2],'%Y-%m-%d')-birthdat
                #result_age.iloc[p,j]=(difference.days + difference.seconds/86400)/365.2425
result_date.to_csv(Path+file+'_'+marker+' date.csv')        
result_disease.to_csv(Path+file+'_'+marker+' event.csv')        
#result_age.to_csv('/Users/jadonzhou/Research Projects/Healthcare Predictives/0. HA Cancer Projects (5+)/Data/comsafter_age.csv')        



import pandas as pd

file_path = "/Volumes/T7/OPRI UK/Objective 9/Recurrence/cprd_pneumonia_long_table.txt"
dataframe1 = pd.read_csv(file_path, delim_whitespace=True)

dataframe1.to_csv('/Volumes/T7/OPRI UK/Objective 9/Recurrence/cprd_pneumonia_long_table.csv', index = False)














