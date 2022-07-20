import pandas as pd
import numpy as np
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
import scipy.stats as stats
from scipy.stats.mstats import kruskalwallis
from math import floor
from scipy.stats import chi2_contingency

# Prednisolone equvalent
Data = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/patid.csv", encoding='windows-1252')
#Data=Data.iloc[67000:len(Data['patid'].values.tolist()),]
Consultations_gp_surgery = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Data/cumulative dosages/Drugdata.csv", encoding='windows-1252')
Consultations_gp_surgery=Consultations_gp_surgery[Consultations_gp_surgery['patid'].isin(Data['patid'].values.tolist())]
Consultations_gp_surgery=Consultations_gp_surgery[Consultations_gp_surgery['routine_copd_rx']==1]
#Consultations_gp_surgery['productname'][Consultations_gp_surgery['productname']=='Cortisone 5mg capsules']
#Consultations_gp_surgery=Consultations_gp_surgery[Consultations_gp_surgery['resp_review']==0]
CGPResults=pd.DataFrame(np.zeros((Data.shape[0],4)),columns=[['patid','Number of non-acute prescriptions','Cumulative prednisolone equvalent non-acute dosage, mg','Cumulative prednisolone equvalent non-acute duration, days']])
for i in range(len(Data['patid'].values.tolist())):
    print(i)
    CGPTemp=Consultations_gp_surgery[Consultations_gp_surgery['patid']==Data.iloc[i,1]]
    CGPResults.iloc[i,0]=Data.iloc[i,1]
    if len(CGPTemp):
        CGPResults.iloc[i,1]=len(CGPTemp)
        CGPResults.iloc[i,2]=CGPTemp['Prednisolone equvalent dosage'].sum()
        CGPResults.iloc[i,3]=CGPTemp['Dose duration'].sum()
    else:
        CGPResults.iloc[i,1]=0
        CGPResults.iloc[i,2]=""
        CGPResults.iloc[i,3]=""
CGPResults.to_csv("/Users/jadonzhou/Research Projects/OPRI UK/Data/cumulative dosages/Prednisolone equvalent non-acute medication statistics.csv")









