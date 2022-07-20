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


# calculate eos count changes
database = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 6/1205/Database.csv")
EOSData = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 6/1205/cprd_eosinophils_all_20211203.csv")
EOSDataCohort=EOSData[EOSData['patid'].isin(database['patid'].values.tolist())]
EOSDataCohort=EOSDataCohort.drop_duplicates()
Results=[]
for p in range(database.shape[0]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    tempEOSData=EOSDataCohort[EOSDataCohort['patid']==database.iloc[p,0]]
    if len(tempEOSData):
        print(p)
        tempEOSDataBefore=tempEOSData[tempEOSData['EventDate']<database.iloc[p,1]]     
        tempEOSDataAfter=tempEOSData[tempEOSData['EventDate']>=database.iloc[p,1]]
        maximumBefore=0
        if len(tempEOSDataBefore)>0:
            maximumBefore=tempEOSDataBefore['numeric_1'].max()
        else:
            maximumBefore=0
        minimumAfter=0
        if len(tempEOSDataAfter)>0:
            minimumAfter=tempEOSDataAfter['numeric_1'].min()
        else:
            minimumAfter=0
        Results.append([database.iloc[p,0],maximumBefore,minimumAfter])
    else:
        Results.append([database.iloc[p,0],'NA','NA'])
Results=pd.DataFrame(Results)
Results.columns=['patid','Maximum eosinophil during exacerbation', 'Minimum eosinophil after exacerbation']
Results.to_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 6/1205/eosinophil count changes 1205.csv")


Data = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/patid.csv", encoding='windows-1252')
#Data=Data.iloc[67000:len(Data['patid'].values.tolist()),]
Consultations_gp_surgery = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Data/drugsubstances/Cortisone Acetate.csv", encoding='windows-1252')
Consultations_gp_surgery=Consultations_gp_surgery[Consultations_gp_surgery['patid'].isin(Data['patid'].values.tolist())]
Consultations_gp_surgery=Consultations_gp_surgery[Consultations_gp_surgery['resp_event']==1]
productnames=np.unique(Consultations_gp_surgery['productname'].tolist()).tolist()
#Consultations_gp_surgery['productname'][Consultations_gp_surgery['productname']=='Cortisone 5mg capsules']
#Consultations_gp_surgery=Consultations_gp_surgery[Consultations_gp_surgery['resp_review']==0]
CGPResults=pd.DataFrame(np.zeros((Data.shape[0],4)),columns=[['patid','Number of prescriptions','Cumulative dosage, mg','Cumulative duration, days']])
for i in range(len(Data['patid'].values.tolist())):
    print(i)
    CGPTemp=Consultations_gp_surgery[Consultations_gp_surgery['patid']==Data.iloc[i,0]]
    CGPResults.iloc[i,0]=Data.iloc[i,0]
    if len(CGPTemp):
        CGPTemp=CGPTemp.sort_values(by = 'eventdate',ascending=True)
        CGPResults.iloc[i,1]=len(CGPTemp)
        CGPResults.iloc[i,2]=CGPTemp['qty'].sum()*25
        CGPResults.iloc[i,3]=CGPTemp['dose_duration'].sum()
    else:
        CGPResults.iloc[i,1]=0
        CGPResults.iloc[i,2]=""
        CGPResults.iloc[i,3]=""
CGPResults.to_csv("/Users/jadonzhou/Research Projects/OPRI UK/Data/cumulative dosages/Cortisone Acetate statistics.csv")



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
        
   
    
database = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/patid.csv")
EDCauses=pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/EDCauses.csv")
EDData = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_outpatient_visits.csv")
EDDataCohort=EDData[EDData['patid'].isin(database['patid'].values.tolist())]
EDDataCohort=EDDataCohort.drop_duplicates()
EDResults=pd.DataFrame(np.zeros((database.shape[0],EDCauses.shape[1])),columns=EDCauses.columns)
for p in range(database.shape[0]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    comorbidities=EDDataCohort[EDDataCohort['patid']==database.iloc[p,1]]
    if len(comorbidities):
        print(p)
    for i in range(EDCauses.shape[1]):
        tempcomorbidities=comorbidities[comorbidities['tretspef'].isin(EDCauses.iloc[:,i].dropna().tolist())]
        EDResults.iloc[p,i]=len(tempcomorbidities)
EDResults.to_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_outpatient_visits statistics 1126.csv")



# extract Maintenance Therapies before and after COPD
database = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 6/1205/Database.csv")
DrugData = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 6/1205/cprd_20_159_out_ba_drugs_20211203.csv")
EDDataResult=[]
i=1
for p in range(database.shape[0]):
    tempdrug=DrugData[DrugData['patid']==database.iloc[p,0]]
    if len(tempdrug)>0:
        # before or after COPD
        tempdrug=tempdrug[tempdrug['eventdate']<database.iloc[p,1]]
        tempdrug = tempdrug.sort_values(by = 'eventdate',ascending=True)
        #stringwant=','.join(tempdrug['cat\n'])
        EDDataResult.append([database.iloc[p,0], ','.join(tempdrug['cat\n'].tolist()).replace('\n','').replace('/','+')])
    else:
        EDDataResult.append([database.iloc[p,0], ''])
    i=i+1
    print(i)    
EDDataResult=pd.DataFrame(EDDataResult)
EDDataResult.columns=['patid','variables']
EDDataResult.to_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 6/1205/cprd_20_159_out_ba_drugs_20211203_before_COPD.csv")


# extract Maintenance Therapies before and after COPD
database = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 6/1205/Database.csv")
DrugData = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 6/1205/cprd_20_159_out_ba_drugs_20211203_after_COPD.csv")
EDDataResult=[]
i=1
for p in range(database.shape[0]):
    tempdrug=DrugData['variables'][DrugData['patid']==database.iloc[p,0]].values[0]
    if 'AAAAA'!=tempdrug:
        EDDataResult.append([database.iloc[p,0], tempdrug.replace('\n','')])
    else:
        EDDataResult.append([database.iloc[p,0], ''])
    i=i+1
    print(i)    
EDDataResult=pd.DataFrame(EDDataResult)
EDDataResult.columns=['patid','variables']
EDDataResult.to_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 6/1205/cprd_20_159_out_ba_drugs_20211203_after_COPD_new.csv")


# calculate Maintenance Therapies
database = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 6/1205/Database.csv")
EDCauses=pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 6/1205/MaintenanceTherapies.csv")
EDData = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 6/1205/cprd_20_159_out_ba_drugs_20211203_after_COPD_new.csv")
EDDataCohort=EDData[EDData['patid'].isin(database['patid'].values.tolist())]
EDDataCohort=EDDataCohort.drop_duplicates()
EDResults=pd.DataFrame(np.zeros((database.shape[0],EDCauses.shape[1])),columns=EDCauses.columns)
for p in range(database.shape[0]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    comorbidities=EDDataCohort[EDDataCohort['patid']==database.iloc[p,0]]
    if 'AAAAA'!=comorbidities['variables'].tolist()[0]:
        print(p)
        length=len(comorbidities['variables'].tolist()[0].split(','))-1
        tempCom=comorbidities['variables'].tolist()[0].split(',')[3:length]
        for i in range(EDCauses.shape[1]):
            causes=EDCauses.iloc[:,i].dropna().tolist()
            numCause=0
            for cau in causes:
                for k in range(len(tempCom)-1):
                    str=tempCom[k]+','+tempCom[k+1]
                    if str==cau:
                        numCause=numCause+1  
            EDResults.iloc[p,i]=numCause
    else:
        EDResults.iloc[p,0]=''
        EDResults.iloc[p,1]=''
        EDResults.iloc[p,2]=''
        EDResults.iloc[p,3]=''
EDResults.to_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 6/1205/Maintenance therapies statistics 1216 after COPD.csv")


numCause=0
for cau in causes:
    print(cau+": "+str(comorbidities['variables'].tolist()[0].count(cau)))
    numCause=numCause+comorbidities['variables'].tolist()[0].count(cau)
    
# number of drugsubstances
database = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/patid.csv")
EDCauses=pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/Antibiotics drugs.csv")
EDData = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Data/Downloads/cprd_long_scs_20210129.csv")
EDDataCohort=EDData[EDData['patid'].isin(database['patid'].values.tolist())]
EDDataCohort=EDDataCohort.drop_duplicates()
drugs=pd.DataFrame(np.unique(EDDataCohort['drugsubstance'].tolist()).tolist())
EDResults=pd.DataFrame(np.zeros((database.shape[0],EDCauses.shape[1])),columns=EDCauses.columns)
for p in range(database.shape[0]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    comorbidities=EDDataCohort[EDDataCohort['patid']==database.iloc[p,1]]
    if len(comorbidities):
        print(p)
        for i in range(EDCauses.shape[1]):
            tempcomorbidities=comorbidities[comorbidities['drugsubstance'].isin(EDCauses.iloc[:,i].dropna().tolist())]
            EDResults.iloc[p,i]=len(tempcomorbidities)
EDResults.to_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_drug_substance statistics 1130.csv")



# number of antibiotics drugs'
database = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/patid.csv")
EDCauses=pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/Antibiotics drugs.csv")
EDData = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/cprd_all_antibiotic_courses_post_20211125.csv")
#EDData=EDData.iloc[:,1].str.split(',',expand=True)
#EDData.columns=EDData.iloc[0,:]
#EDData=EDData[EDData['resp_review']==1]
EDDataCohort=EDData[EDData['patid'].isin(database['patid'].values.tolist())]
EDDataCohort=EDDataCohort.drop_duplicates()
EDResults=pd.DataFrame(np.zeros((database.shape[0],1)),columns=['Number of antibiotics drugs'])
StartDates=[]
LastDates=[]
for p in range(database.shape[0]):
    #birthdat=datetime.strptime(database.iloc[p,2],'%Y/%m/%d')
    comorbidities=EDDataCohort[EDDataCohort['patid']==database.iloc[p,1]]
    comorbidities=comorbidities.sort_values(by = 'eventdate',ascending=True)
    length=len(comorbidities)
    EDResults.iloc[p,0]=length
    if len(comorbidities):
        print(p)
        StartDates.append(comorbidities['eventdate'].tolist()[0])
        LastDates.append(comorbidities['eventdate'].tolist()[length-1])
    else:
        StartDates.append("")
        LastDates.append("")
EDResults['Start Date']=pd.DataFrame(StartDates)
EDResults['End Date']=pd.DataFrame(LastDates)
EDResults.to_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/cprd_all_antibiotic_overall_statistics_1130.csv")




    


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






database = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/patid.csv")
icd10codes=pd.read_csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/Tools/Comorbidity/ICD10Codes.csv")
InpatientData = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/cprd_out_inpatient_20210804.csv")
InpatientDataCohort=InpatientData[InpatientData['patid'].isin(database['patid'].values.tolist())]
#InpatientDataCohort=InpatientDataCohort[InpatientDataCohort['disease_cat admission_type']=='elective']
InpatientDataCohort=InpatientDataCohort.drop_duplicates()
InpatientResults=pd.DataFrame(np.zeros((database.shape[0],icd10codes.shape[1])),columns=icd10codes.columns)
pat=0
for p in range(database.shape[0]):
    print(pat)
    comorbidities=InpatientDataCohort[InpatientDataCohort['patid']==database.iloc[p,1]]
    for i in range(icd10codes.shape[1]):
        tempcomorbidities=comorbidities[comorbidities['ICD_PRIMARY'].isin(icd10codes.iloc[:,i].dropna().tolist())]
        if len(tempcomorbidities):
            InpatientResults.iloc[p,i]=1
        else:
            InpatientResults.iloc[p,i]=0
    pat=pat+1
InpatientResults.to_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 6/Inpatient Dx Statistics ICD-10.csv")





database = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/patid.csv")
icd10codes=pd.read_csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/Tools/Comorbidity/ICD10Codes.csv")
InpatientData = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_inpatient_20210928.csv")
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
            tempcomorbidities=comorbidities[comorbidities['ICD_PRIMARY'].isin(icd10codes.iloc[:,i].dropna().tolist())]
            InpatientResults.iloc[p,0]=len(tempcomorbidities[tempcomorbidities['length_of_stay']==0])
            InpatientResults.iloc[p,1]=len(tempcomorbidities[tempcomorbidities['length_of_stay']>=1])
            InpatientResults.iloc[p,2]=len(tempcomorbidities[tempcomorbidities['length_of_stay']<=1])
            InpatientResults.iloc[p,3]=len(tempcomorbidities[tempcomorbidities['length_of_stay']>=2])
            InpatientResults.iloc[p,4]=database.iloc[p,1]
        else:
            InpatientResults.iloc[p,4]=database.iloc[p,1]
        print(database.iloc[p,1])    
    InpatientResults.to_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/non-elective/non-elective_"+icd10codes.columns[i]+".csv")
    
    
database = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/patid.csv")
icd10codes=pd.read_csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/Tools/Comorbidity/ICD10Codes.csv")
InpatientData = pd.read_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/cprd_out_inpatient_20210928.csv")
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
            tempcomorbidities=comorbidities[comorbidities['ICD_PRIMARY'].isin(icd10codes.iloc[:,i].dropna().tolist())]
            InpatientResults.iloc[p,0]=len(tempcomorbidities[tempcomorbidities['length_of_stay']==0])
            InpatientResults.iloc[p,1]=len(tempcomorbidities[tempcomorbidities['length_of_stay']>=1])
            InpatientResults.iloc[p,2]=len(tempcomorbidities[tempcomorbidities['length_of_stay']<=1])
            InpatientResults.iloc[p,3]=len(tempcomorbidities[tempcomorbidities['length_of_stay']>=2])
            InpatientResults.iloc[p,4]=database.iloc[p,1]
        else:
            InpatientResults.iloc[p,4]=database.iloc[p,1]
        print(database.iloc[p,1])    
    InpatientResults.to_csv("/Users/jadonzhou/Research Projects/OPRI UK/Objective 3/objective3_outcome_tables/elective/elective_"+icd10codes.columns[i]+".csv")
    
    


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





database = pd.read_csv("/Volumes/T7/OPRI UK/Objective 6/HES linkage status.csv")
icd10codes=pd.read_csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/Tools/Comorbidity/ICD10Codes.csv")
InpatientData = pd.read_csv("/Volumes/T7/OPRI UK/Objective 6/CPRD Database outcome.csv")
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
        
    













