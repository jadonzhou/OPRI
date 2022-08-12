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
Data=Data.iloc[67000:len(Data['patid'].values.tolist()),]