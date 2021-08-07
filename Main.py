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


Data = pd.read_csv("/Volumes/T7/OPRI UK/Objective 2/CPRD Database.csv", encoding='windows-1252')
EmergVisits = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_accid_emerg_visits.csv", encoding='windows-1252')
uniqueAE=np.unique(EmergVisits['ae_area_code'].values.tolist()).tolist()
EmergVisitsResults=pd.DataFrame(np.zeros((Data.shape[0],len(uniqueAE))),columns=uniqueAE)
Combined_outcomes = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/cprd_20_159_combined_outcomes.csv", encoding='windows-1252')
Consultations_gp_surgery = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_consultations_gp_surgery.csv", encoding='windows-1252')
Consultations_gp_surgery.columns=Consultations_gp_surgery.iloc[0,]
uniqueCGP=np.unique(Consultations_gp_surgery['con_setting\n'].values.tolist()).tolist()
CGPResults=pd.DataFrame(np.zeros((Data.shape[0],len(uniqueCGP))),columns=uniqueCGP)
Inpatient = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_inpatient.csv", encoding='windows-1252')
uniqueInpatient=np.unique(Inpatient['ICD_PRIMARY'].values.tolist()).tolist()
InpatientResults=pd.DataFrame(np.zeros((Data.shape[0],len(uniqueInpatient))),columns=uniqueInpatient)
Outpatient_visits = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_outpatient_visits.csv", encoding='windows-1252')
uniqueOutpatient=np.unique(Outpatient_visits['mainspef_dscr'].values.tolist()).tolist()
OutpatientResults=pd.DataFrame(np.zeros((Data.shape[0],len(uniqueOutpatient))),columns=uniqueOutpatient)
for i in range(len(Data['patid'].values.tolist())):
    print(i)
    EmergVisitsTemp=EmergVisits[EmergVisits['patid']==Data.iloc[i,0]]
    for col in range(len(uniqueAE)):
        EmergVisitsResults.iloc[i,col]=len(EmergVisitsTemp[EmergVisitsTemp['ae_area_code']==uniqueAE[col]])
    CGPTemp=Consultations_gp_surgery[Consultations_gp_surgery['patid']==Data.iloc[i,0]]
    for col in range(len(uniqueCGP)):
        CGPResults.iloc[i,col]=len(CGPTemp[CGPTemp['con_setting\n']==uniqueCGP[col]])
    OutpatientTemp=Outpatient_visits[Outpatient_visits['patid']==Data.iloc[i,0]]
    for col in range(len(uniqueOutpatient)):
        OutpatientResults.iloc[i,col]=len(OutpatientTemp[OutpatientTemp['mainspef_dscr']==uniqueOutpatient[col]])
EmergVisitsTemp.to_csv("/Volumes/T7/OPRI UK/Objective 3/EmergVisitsTemp.csv")
CGPResults.to_csv("/Volumes/T7/OPRI UK/Objective 3/CGPResults.csv")
OutpatientResults.to_csv("/Volumes/T7/OPRI UK/Objective 3/OutpatientResults new.csv")


Data = pd.read_csv("/Volumes/T7/OPRI UK/Objective 2/CPRD Database.csv", encoding='windows-1252')
Inpatient = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_inpatient.csv", encoding='windows-1252')
InpatientResults=[]
InpatientCohort=Inpatient[Inpatient['length_of_stay']==1]
i=0
for patient in Data['patid'].values.tolist():
    i=i+1
    print(i)
    temp=InpatientCohort[InpatientCohort['patid']==patient]
    InpatientResults.append(len(temp))
pd.DataFrame(Data['patid']).to_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/patid.csv")
        
    














