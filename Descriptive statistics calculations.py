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



Path="/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/"
Data = pd.read_csv(Path+"patid.csv", encoding='windows-1252')
temp = pd.read_csv(Path+"cprd_out_inpatient_20210804.csv", encoding='windows-1252')
Datafinal=temp[temp['patid'].isin(Data['patid'].values.tolist())]
#temp=temp[['patid', 'end_of_follow_up_dte', 'end_of_follow_up_days']]
Datafinal=pd.merge(pd.DataFrame(Data['patid']), temp, how = 'left', on='patid')
Datafinal.to_csv(Path+"cprd_out_inpatient_data.csv")


Data = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/patid.csv")
Inpatient = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_inpatient_data.csv", encoding='windows-1252')
InpatientCohort=Inpatient[Inpatient['admission_type']=='non-elective']
InpatientCohort=Inpatient[Inpatient['length_of_stay']>=2]
InpatientResults=[]
i=0
for patient in Data['patid'].values.tolist():
    i=i+1
    print(i)
    temp=InpatientCohort[InpatientCohort['patid']==int(patient)]
    InpatientResults.append([patient, len(temp)])
pd.DataFrame(InpatientResults).to_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/elective long more or equal  2.csv")
        
    


database = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/patid.csv")
EDCauses=pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/EDCauses.csv")
EDData = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_accid_emerg_visits.csv")
EDDataCohort=EDData[EDData['patid'].isin(database['patid'].values.tolist())]
EDDataCohort=EDDataCohort.drop_duplicates()
EDResults=pd.DataFrame(np.zeros((database.shape[0],EDCauses.shape[1])),columns=EDCauses.columns)
for p in range(database.shape[0]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    comorbidities=EDDataCohort[EDDataCohort['patid']==database.iloc[p,1]]
    if len(comorbidities):
        print(p)
    for i in range(EDCauses.shape[1]):
        tempcomorbidities=comorbidities[comorbidities['ae_area_code'].isin(EDCauses.iloc[:,i].dropna().tolist())]
        EDResults.iloc[p,i]=len(tempcomorbidities)
EDResults.to_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/EDDataCohort count 0915.csv")






database = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/patid.csv")
icd10codes=pd.read_csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/Tools/Comorbidity/ICD10Codes.csv")
InpatientData = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_inpatient_20210928.csv")
InpatientDataCohort=InpatientData[InpatientData['patid'].isin(database['patid'].values.tolist())]
#InpatientDataCohort=InpatientDataCohort[InpatientDataCohort['disease_cat admission_type']=='elective']
InpatientDataCohort=InpatientDataCohort.drop_duplicates()
InpatientDataCohort.shape
InpatientResults=pd.DataFrame(np.zeros((database.shape[0],icd10codes.shape[1])),columns=icd10codes.columns)
for i in range(icd10codes.shape[1]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    InpatientResults=pd.DataFrame(np.zeros((database.shape[0],5)),columns=['LOS=0','LOS>=1','LOS<=1','LOS>=2','patid'])
    for p in range(database.shape[0]):
        comorbidities=InpatientDataCohort[InpatientDataCohort['patid']==database.iloc[p,1]]
        if len(comorbidities):
            tempcomorbidities=comorbidities[comorbidities['ICD_PRIMARY'].isin(icd10codes.iloc[:,i].dropna().tolist())]
            InpatientResults.iloc[p,0]=len(tempcomorbidities[tempcomorbidities['length_of_stay']==0])
            InpatientResults.iloc[p,1]=len(tempcomorbidities[tempcomorbidities['length_of_stay']>=1])
            InpatientResults.iloc[p,2]=len(tempcomorbidities[tempcomorbidities['length_of_stay']<=1])
            InpatientResults.iloc[p,3]=len(tempcomorbidities[tempcomorbidities['length_of_stay']>=2])
            InpatientResults.iloc[p,4]=database.iloc[p,1]
        else:
            InpatientResults.iloc[p,4]=database.iloc[p,1]
        print(database.iloc[p,1])    
    InpatientResults.to_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/allcauses/"+icd10codes.columns[i]+"_allcauses.csv")





database = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/patid.csv")
icd10codes=pd.read_csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/Tools/Comorbidity/ICD10Codes.csv")
InpatientData = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_inpatient_20210928.csv")
InpatientDataCohort=InpatientData[InpatientData['patid'].isin(database['patid'].values.tolist())]
InpatientDataCohort=InpatientDataCohort[InpatientDataCohort['disease_cat admission_type']=='non-elective']
InpatientDataCohort=InpatientDataCohort.drop_duplicates()
InpatientDataCohort.shape
InpatientResults=pd.DataFrame(np.zeros((database.shape[0],icd10codes.shape[1])),columns=icd10codes.columns)
for i in range(icd10codes.shape[1]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    InpatientResults=pd.DataFrame(np.zeros((database.shape[0],5)),columns=['LOS=0','LOS>=1','LOS<=1','LOS>=2','patid'])
    for p in range(database.shape[0]):
        comorbidities=InpatientDataCohort[InpatientDataCohort['patid']==database.iloc[p,1]]
        if len(comorbidities):
            #tempcomorbidities=comorbidities[comorbidities['ICD_PRIMARY'].isin(icd10codes.iloc[:,i].dropna().tolist())]
            tempcomorbidities=comorbidities
            InpatientResults.iloc[p,0]=len(tempcomorbidities[tempcomorbidities['length_of_stay']==0])
            InpatientResults.iloc[p,1]=len(tempcomorbidities[tempcomorbidities['length_of_stay']>=1])
            InpatientResults.iloc[p,2]=len(tempcomorbidities[tempcomorbidities['length_of_stay']<=1])
            InpatientResults.iloc[p,3]=len(tempcomorbidities[tempcomorbidities['length_of_stay']>=2])
            InpatientResults.iloc[p,4]=database.iloc[p,1]
        else:
            InpatientResults.iloc[p,4]=database.iloc[p,1]
        print(database.iloc[p,1])    
    InpatientResults.to_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/non-elective/"+"non-elective_allcauses.csv")
    
    
database = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/patid.csv")
icd10codes=pd.read_csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/Tools/Comorbidity/ICD10Codes.csv")
InpatientData = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_inpatient_20210928.csv")
InpatientDataCohort=InpatientData[InpatientData['patid'].isin(database['patid'].values.tolist())]
InpatientDataCohort=InpatientDataCohort[InpatientDataCohort['disease_cat admission_type']=='elective']
InpatientDataCohort=InpatientDataCohort.drop_duplicates()
InpatientDataCohort.shape
InpatientResults=pd.DataFrame(np.zeros((database.shape[0],icd10codes.shape[1])),columns=icd10codes.columns)
for i in range(icd10codes.shape[1]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    InpatientResults=pd.DataFrame(np.zeros((database.shape[0],5)),columns=['LOS=0','LOS>=1','LOS<=1','LOS>=2','patid'])
    for p in range(database.shape[0]):
        comorbidities=InpatientDataCohort[InpatientDataCohort['patid']==database.iloc[p,1]]
        if len(comorbidities):
            #tempcomorbidities=comorbidities[comorbidities['ICD_PRIMARY'].isin(icd10codes.iloc[:,i].dropna().tolist())]
            tempcomorbidities=comorbidities
            InpatientResults.iloc[p,0]=len(tempcomorbidities[tempcomorbidities['length_of_stay']==0])
            InpatientResults.iloc[p,1]=len(tempcomorbidities[tempcomorbidities['length_of_stay']>=1])
            InpatientResults.iloc[p,2]=len(tempcomorbidities[tempcomorbidities['length_of_stay']<=1])
            InpatientResults.iloc[p,3]=len(tempcomorbidities[tempcomorbidities['length_of_stay']>=2])
            InpatientResults.iloc[p,4]=database.iloc[p,1]
        else:
            InpatientResults.iloc[p,4]=database.iloc[p,1]
        print(database.iloc[p,1])    
    InpatientResults.to_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/elective/"+"elective_allcauses.csv")
    
    


counts = pd.read_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/InpatientDataCohort count.csv")
comCategory = pd.read_csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/Tools/Comorbidity/ICD10Codes.csv", encoding='windows-1252')
comCategory=comCategory.astype(str)
comCategorys=pd.concat(comCategory.iloc[:,i] for i in range(comCategory.shape[1])).tolist()
results=[]
for j in range(comCategory.shape[1]):
    temp=counts[counts['ICD_PRIMARY'].isin(comCategory.iloc[:,j].dropna().tolist())]
    results.append(temp['Number of patients'].sum())


result_date.to_csv(Path+file+' '+marker+' date.csv')        
result_disease.to_csv(Path+file+' '+marker+' event.csv')        
#result_age.to_csv('/Users/jadonzhou/Research Projects/Healthcare Predictives/0. HA Cancer Projects (5+)/Data/comsafter_age.csv')        






uniqueAE=np.unique(EDData['ae_area_code'].values.tolist()).tolist()


InpatientCohort=Inpatient[Inpatient['admission_type']=='non-elective']
InpatientCohort=Inpatient[Inpatient['length_of_stay']>=2]
InpatientResults=[]
i=0
for patient in Data['patid'].values.tolist():
    i=i+1
    print(i)
    temp=InpatientCohort[InpatientCohort['patid']==int(patient)]
    InpatientResults.append([patient, len(temp)])
pd.DataFrame(InpatientResults).to_csv("/Volumes/T7/OPRI UK/Objective 3/objective3_outcome_tables/elective long more or equal  2.csv")
        
    













