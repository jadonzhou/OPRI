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
marker="read codes for MI 20142015 120-day rule"
database = pd.read_csv(Path+file+".csv")
database['Reference Key']=database['patid']
database['Reference Date']=database['idx_dte']
#database['Baseline Date'] = pd.to_datetime(database['Baseline Date'])
#comCategory = pd.read_csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/Tools/Comorbidity/ICD10Codes.csv", encoding='windows-1252')
#comCategory = comCategory.iloc[:,0:2]
#comCategory = pd.read_csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/Tools/Comorbidity/HA Prior Comorbidities.csv", encoding='windows-1252')
#comCategory=comCategory.astype(str)
#comCategorys=pd.concat(comCategory.iloc[:,i] for i in range(comCategory.shape[1])).tolist()
Dx = pd.read_csv("/Volumes/T7/OPRI UK/Objective 9/cprd_MI_long_table with read code copy 20142015.csv")
Dx = Dx.apply(lambda col: pd.to_datetime(col, errors='ignore') 
              if col.dtypes == object 
              else col, 
              axis=0)
#Dx.to_csv("/Volumes/T7/OPRI UK/Objective 9/cprd_MI_long_table with read code copy.csv", index=False)
Dx=Dx[Dx['patid'].isin(database['patid'].tolist())]
#Dx=Dx[Dx['medcode'].isnull()]
#result_age=pd.DataFrame(np.zeros((databas ane.shape[0],comCategory.shape[1])))
#result_age.columns=comCategory.columns
result_disease=pd.DataFrame(np.zeros((database.shape[0],3)))
result_disease.columns=['patid', 'Number of MI events', 'Number of MI events (120-day rule applied)']
result_date=pd.DataFrame(np.zeros((database.shape[0],2)))
result_date.columns=['patid', 'Dates of MI events']
for p in range(database.shape[0]):
    print(p)
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    comorbidities=Dx[(Dx['patid']==database.iloc[p,0]) | (Dx['patid']==str(database.iloc[p,0]))]
    comorbidities=comorbidities.sort_values(by='eventdate',ascending=True)
    baselineDate=database.iloc[p,1]
    #comorbidities = comorbidities[(comorbidities['eventdate']>=pd.to_datetime(baselineDate))]
    result_disease.iloc[p,0]=database.iloc[p,0]
    result_disease.iloc[p,1]=comorbidities.shape[0]
    result_date.iloc[p,0]=database.iloc[p,0]
    result_date.iloc[p,1]=",".join([x.strftime('%Y/%m/%d') for x in comorbidities['eventdate']])
    dates=[x.days for x in comorbidities['eventdate'].diff()]
    dates=[x for x in dates if x>=120]
    result_disease.iloc[p,2]=len(dates)+1
result_date.to_csv(Path+file+'_'+marker+' date.csv')        
result_disease.to_csv(Path+file+'_'+marker+' event.csv')        
#result_age.to_csv('/Users/jadonzhou/Research Projects/Healthcare Predictives/0. HA Cancer Projects (5+)/Data/comsafter_age.csv')        


