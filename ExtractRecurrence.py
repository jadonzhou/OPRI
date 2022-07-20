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

# =============================================================================
# osteoporosis
# =============================================================================
Path="/Volumes/T7/OPRI UK/Objective 9/Recurrence/"
file="COPD general 6 new"
marker="prior osteoporosis for recurrence"
database=pd.read_csv(Path+file+".csv")
database=database.apply(lambda col: pd.to_datetime(col, errors='ignore') 
              if col.dtypes == object 
              else col, 
              axis=0)
Dx=pd.read_csv("/Volumes/T7/OPRI UK/Objective 9/Recurrence/cprd_osteoporosis_fracture_long_table.csv")
Dx['idx_dte'] = pd.to_datetime(Dx['idx_dte'])
Dx['eventdate'] = pd.to_datetime(Dx['eventdate'])
Dx = Dx.sort_values(by = 'idx_dte',ascending=True)
result_disease=pd.DataFrame(np.zeros((database.shape[0],1)))
result_disease.index=database['patid'].values.tolist()
result_date=pd.DataFrame(np.zeros((database.shape[0],1)))
result_date.index=database['idx_dte'].values.tolist()
for p in range(database.shape[0]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    baselineDate=database.iloc[p,1]
    comorbidities=Dx[(Dx['patid']==database.iloc[p,0]) | (Dx['patid']==str(database.iloc[p,0]))]
    comorbidities = comorbidities[(comorbidities['eventdate']<=baselineDate)]
    #comorbidities=comorbidities[comorbidities['idx_dte']>=pd.to_datetime(baselineDate)-datetime.timedelta(days = 28)] # within 28 days before index date
    comorbidities=comorbidities.sort_values(by = 'eventdate',ascending=False)
    if comorbidities.shape[0]>0:
        print(p)
        result_disease.iloc[p,0]=1
        result_date.iloc[p,0]=comorbidities.iloc[0,3]
result_date.to_csv(Path+file+'_'+marker+' date.csv')        
result_disease.to_csv(Path+file+'_'+marker+' event.csv')        
#result_age.to_csv('/Users/jadonzhou/Research Projects/Healthcare Predictives/0. HA Cancer Projects (5+)/Data/comsafter_age.csv')        


Path="/Volumes/T7/OPRI UK/Objective 9/Recurrence/"
file="COPD general 6 new"
marker="outcome osteoporosis for recurrence"
database=pd.read_csv(Path+file+".csv")
database=database.apply(lambda col: pd.to_datetime(col, errors='ignore') 
              if col.dtypes == object 
              else col, 
              axis=0)
Dx=pd.read_csv("/Volumes/T7/OPRI UK/Objective 9/Recurrence/cprd_osteoporosis_fracture_long_table.csv")
Dx['idx_dte'] = pd.to_datetime(Dx['idx_dte'])
Dx['eventdate'] = pd.to_datetime(Dx['eventdate'])
Dx = Dx.sort_values(by = 'idx_dte',ascending=True)
result_disease=pd.DataFrame(np.zeros((database.shape[0],1)))
result_disease.index=database['patid'].values.tolist()
result_date=pd.DataFrame(np.zeros((database.shape[0],1)))
result_date.index=database['idx_dte'].values.tolist()
for p in range(database.shape[0]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    baselineDate=database.iloc[p,1]
    comorbidities=Dx[(Dx['patid']==database.iloc[p,0]) | (Dx['patid']==str(database.iloc[p,0]))]
    comorbidities = comorbidities[(comorbidities['eventdate']>baselineDate)]
    #comorbidities=comorbidities[comorbidities['idx_dte']>=pd.to_datetime(baselineDate)-datetime.timedelta(days = 28)] # within 28 days before index date
    comorbidities=comorbidities.sort_values(by = 'eventdate',ascending=False)
    if comorbidities.shape[0]>0:
        print(p)
        result_disease.iloc[p,0]=1
        result_date.iloc[p,0]=comorbidities.iloc[0,3]
result_date.to_csv(Path+file+'_'+marker+' date.csv')        
result_disease.to_csv(Path+file+'_'+marker+' event.csv')        
#result_age.to_csv('/Users/jadonzhou/Research Projects/Healthcare Predictives/0. HA Cancer Projects (5+)/Data/comsafter_age.csv')        



# =============================================================================
# pneumonia
# =============================================================================
Path="/Volumes/T7/OPRI UK/Objective 9/Recurrence/"
file="COPD general 6 new"
marker="prior pneumonia for recurrence"
database=pd.read_csv(Path+file+".csv")
database=database.apply(lambda col: pd.to_datetime(col, errors='ignore') 
              if col.dtypes == object 
              else col, 
              axis=0)
Dx=pd.read_csv("/Volumes/T7/OPRI UK/Objective 9/Recurrence/cprd_pneumonia_long_table.csv")
Dx['idx_dte'] = pd.to_datetime(Dx['idx_dte'])
Dx['eventdate'] = pd.to_datetime(Dx['eventdate'])
Dx = Dx.sort_values(by = 'idx_dte',ascending=True)
result_disease=pd.DataFrame(np.zeros((database.shape[0],1)))
result_disease.index=database['patid'].values.tolist()
result_date=pd.DataFrame(np.zeros((database.shape[0],1)))
result_date.index=database['idx_dte'].values.tolist()
for p in range(database.shape[0]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    baselineDate=database.iloc[p,1]
    comorbidities=Dx[(Dx['patid']==database.iloc[p,0]) | (Dx['patid']==str(database.iloc[p,0]))]
    comorbidities = comorbidities[(comorbidities['eventdate']<=baselineDate)]
    #comorbidities=comorbidities[comorbidities['idx_dte']>=pd.to_datetime(baselineDate)-datetime.timedelta(days = 28)] # within 28 days before index date
    comorbidities=comorbidities.sort_values(by = 'eventdate',ascending=False)
    if comorbidities.shape[0]>0:
        print(p)
        result_disease.iloc[p,0]=1
        result_date.iloc[p,0]=comorbidities.iloc[0,3]
result_date.to_csv(Path+file+'_'+marker+' date.csv')        
result_disease.to_csv(Path+file+'_'+marker+' event.csv')        
#result_age.to_csv('/Users/jadonzhou/Research Projects/Healthcare Predictives/0. HA Cancer Projects (5+)/Data/comsafter_age.csv')        


Path="/Volumes/T7/OPRI UK/Objective 9/Recurrence/"
file="COPD general 6 new"
marker="outcome pneumonia for recurrence"
database=pd.read_csv(Path+file+".csv")
database=database.apply(lambda col: pd.to_datetime(col, errors='ignore') 
              if col.dtypes == object 
              else col, 
              axis=0)
Dx=pd.read_csv("/Volumes/T7/OPRI UK/Objective 9/Recurrence/cprd_pneumonia_long_table.csv")
Dx['idx_dte'] = pd.to_datetime(Dx['idx_dte'])
Dx['eventdate'] = pd.to_datetime(Dx['eventdate'])
Dx = Dx.sort_values(by = 'idx_dte',ascending=True)
result_disease=pd.DataFrame(np.zeros((database.shape[0],1)))
result_disease.index=database['patid'].values.tolist()
result_date=pd.DataFrame(np.zeros((database.shape[0],1)))
result_date.index=database['idx_dte'].values.tolist()
for p in range(database.shape[0]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    baselineDate=database.iloc[p,1]
    comorbidities=Dx[(Dx['patid']==database.iloc[p,0]) | (Dx['patid']==str(database.iloc[p,0]))]
    comorbidities = comorbidities[(comorbidities['eventdate']>baselineDate)]
    #comorbidities=comorbidities[comorbidities['idx_dte']>=pd.to_datetime(baselineDate)-datetime.timedelta(days = 28)] # within 28 days before index date
    comorbidities=comorbidities.sort_values(by = 'eventdate',ascending=False)
    if comorbidities.shape[0]>0:
        print(p)
        result_disease.iloc[p,0]=1
        result_date.iloc[p,0]=comorbidities.iloc[0,3]
result_date.to_csv(Path+file+'_'+marker+' date.csv')        
result_disease.to_csv(Path+file+'_'+marker+' event.csv')        
#result_age.to_csv('/Users/jadonzhou/Research Projects/Healthcare Predictives/0. HA Cancer Projects (5+)/Data/comsafter_age.csv')        




import csv
with open('/Volumes/T7/OPRI UK/Objective 9/Recurrence/cprd_outcomes_anti_diabetic_meds.txt', 'r') as f:
    content = f.readlines()
    with open('/Volumes/T7/OPRI UK/Objective 9/Recurrence/cprd_outcomes_anti_diabetic_meds.csv', 'w+',  newline = '') as csvFile:
        csvWriter = csv.writer(csvFile, delimiter = ' ')
        Dx=[]
        for elem in content:
            if 'Insulin' not in elem:
                Dx.append(elem.split('\t'))
        Dx=pd.DataFrame(Dx)
        Dx.columns=Dx.iloc[0,:].values.tolist()
        Dx = Dx.drop([Dx.index[0]])
Dx.to_csv("/Volumes/T7/OPRI UK/Objective 9/Recurrence/cprd_outcomes_anti_diabetic_meds_Insulin_excluded.csv", index=False)
            
            


# =============================================================================
# DM
# =============================================================================
Path="/Volumes/T7/OPRI UK/Objective 9/Recurrence/"
file="COPD general 6 new"
marker="prior DM for recurrence"
database=pd.read_csv(Path+file+".csv")
database=database.apply(lambda col: pd.to_datetime(col, errors='ignore') 
              if col.dtypes == object 
              else col, 
              axis=0)
Dx=pd.read_csv("/Volumes/T7/OPRI UK/Objective 9/Recurrence/cprd_outcomes_anti_diabetic_meds_Insulin_excluded.csv")
Dx['idx_dte'] = pd.to_datetime(Dx['idx_dte'])
Dx['eventdate'] = pd.to_datetime(Dx['eventdate'])
Dx = Dx.sort_values(by = 'idx_dte',ascending=True)
result_disease=pd.DataFrame(np.zeros((database.shape[0],1)))
result_disease.index=database['patid'].values.tolist()
result_date=pd.DataFrame(np.zeros((database.shape[0],1)))
result_date.index=database['patid'].values.tolist()
for p in range(database.shape[0]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    baselineDate=database.iloc[p,1]
    comorbidities=Dx[(Dx['patid']==database.iloc[p,0]) | (Dx['patid']==str(database.iloc[p,0]))]
    comorbidities = comorbidities[(comorbidities['eventdate']<=baselineDate)]
    comorbidities=comorbidities.sort_values(by = 'eventdate',ascending=False)
    if comorbidities.shape[0]>0:
        print(p)
        result_disease.iloc[p,0]=1
        result_date.iloc[p,0]=comorbidities.iloc[0,3]
result_date.to_csv(Path+file+'_'+marker+' date.csv')        
result_disease.to_csv(Path+file+'_'+marker+' event.csv')        
#result_age.to_csv('/Users/jadonzhou/Research Projects/Healthcare Predictives/0. HA Cancer Projects (5+)/Data/comsafter_age.csv')        



Path="/Volumes/T7/OPRI UK/Objective 9/Recurrence/"
file="COPD general 6 new"
marker="outcome DM for recurrence"
database=pd.read_csv(Path+file+".csv")
database=database.apply(lambda col: pd.to_datetime(col, errors='ignore') 
              if col.dtypes == object 
              else col, 
              axis=0)
Dx=pd.read_csv("/Volumes/T7/OPRI UK/Objective 9/Recurrence/cprd_outcomes_anti_diabetic_meds_Insulin_excluded.csv")
Dx['idx_dte'] = pd.to_datetime(Dx['idx_dte'])
Dx['eventdate'] = pd.to_datetime(Dx['eventdate'])
Dx = Dx.sort_values(by = 'idx_dte',ascending=True)
result_disease=pd.DataFrame(np.zeros((database.shape[0],1)))
result_disease.index=database['patid'].values.tolist()
result_date=pd.DataFrame(np.zeros((database.shape[0],1)))
result_date.index=database['patid'].values.tolist()
for p in range(database.shape[0]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    baselineDate=database.iloc[p,1]
    comorbidities=Dx[(Dx['patid']==database.iloc[p,0]) | (Dx['patid']==str(database.iloc[p,0]))]
    comorbidities = comorbidities[(comorbidities['eventdate']>baselineDate)]
    comorbidities=comorbidities.sort_values(by = 'eventdate',ascending=False)
    if comorbidities.shape[0]>0:
        print(p)
        result_disease.iloc[p,0]=1
        result_date.iloc[p,0]=comorbidities.iloc[0,3]
result_date.to_csv(Path+file+'_'+marker+' date.csv')        
result_disease.to_csv(Path+file+'_'+marker+' event.csv')        
#result_age.to_csv('/Users/jadonzhou/Research Projects/Healthcare Predictives/0. HA Cancer Projects (5+)/Data/comsafter_age.csv')        







