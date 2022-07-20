library(randomForestSRC)
library(survival)
library(ranger)
library(ggplot2)
library(dplyr)
library(ggfortify)
library(ggRandomForests)
library("survival")
library("survminer")
library(tableone)
library(Matching)
library(survey)
library(reshape2)
library(ggplot2)
# read data
path="/Users/jadonzhou/Research Projects/OPRI UK/Objective 2/CPRD DatabaseOld.csv"
Data <- read.csv(path)
str(Data)
Columns=colnames(Data)
FigureWidth=14
FigureHeight=8
outcomes=c("T2DM","Hypertension")
for (outcome in outcomes){
  Data <- read.csv(path)
  colnames(Data)[which(Columns == outcome)]="Event"
  colnames(Data)[which(Columns == outcome)+1]="Time"
  # Plot cumulative events
  Data$Time=Data$Time/365.5
  Data=Data[Data$Time>=0,]
  Data=Data[Data$Time<20,]
  surv_object <- Surv(time = Data$Time, event = Data$Event)
  fit <- survfit(surv_object ~ Male.gender, data = Data)
  survp=ggsurvplot(fit, 
             conf.int = TRUE,
             #palette = c("#E7B800", "#2E9FDF"),
             ggtheme = theme_bw(),
             legend = "bottom", 
             ylim = c(0.0, 0.8),
             legend.title = " ",
             legend.labs = c("Female","Male"),
             risk.table = TRUE, 
             risk.table.col = "strata",
             fun = "event",)+
    xlab("Year of follow-up")+
    ylab("Cumulative incidence (%)")+
    ggtitle(paste("Cumulative hazard:", outcome))
  quartz.save(file = paste(strsplit(path, "CPRD Database")[[1]][1], outcome, "Gender.jpg"), dpi = 300,width = FigureWidth,height = FigureHeight)
  # Plot cumulative events
  fit <- survfit(surv_object ~ Cumulative.SCS.dosage, data = Data)
  survp=ggsurvplot(fit, 
             conf.int = TRUE,
             #palette = c("#E7B800", "#2E9FDF"),
             ggtheme = theme_bw(),
             legend = "bottom", 
             ylim = c(0.0, 0.8),
             legend.title = " ",
             risk.table = TRUE, 
             risk.table.col = "strata",
             fun = "event",)+
    xlab("Year of follow-up")+
    ylab("Cumulative incidence (%)")+
    ggtitle(paste("Cumulative hazard:", outcome))
  quartz.save(file = paste(strsplit(path, "CPRD Database")[[1]][1], outcome, "Cumulative SCS dosage.jpg"), dpi = 300,width = FigureWidth,height = FigureHeight)
  # Plot cumulative events
  fit <- survfit(surv_object ~ X..7.5_mg_day.1, data = Data)
  survp=ggsurvplot(fit, 
             conf.int = TRUE,
             #palette = c("#E7B800", "#2E9FDF"),
             ggtheme = theme_bw(),
             legend = "bottom", 
             ylim = c(0.0, 0.8),
             legend.title = " ",
             legend.labs = c("Less than 7.5 mg per day","No less than 7.5 mg per day"),
             risk.table = TRUE, 
             risk.table.col = "strata",
             fun = "event",)+
    xlab("Year of follow-up")+
    ylab("Cumulative incidence (%)")+
    ggtitle(paste("Cumulative hazard:", outcome))
  quartz.save(file = paste(strsplit(path, "CPRD Database")[[1]][1], outcome, "Average dosage.jpg"), dpi = 300,width = FigureWidth,height = FigureHeight)
  #ggsave(file = paste(strsplit(path, "CPRD Database")[[1]][1], outcome,"Average dosage.jpg"), print(survp),dpi = 1000)
  # Plot cumulative events
  fit <- survfit(surv_object ~ ABCD, data = Data)
  survp=ggsurvplot(fit, 
             conf.int = TRUE,
             #palette = c("#E7B800", "#2E9FDF"),
             ggtheme = theme_bw(),
             legend = "bottom", 
             ylim = c(0.0, 0.8),
             legend.title = " ",
             risk.table = TRUE, 
             risk.table.col = "strata",
             fun = "event",)+
    xlab("Year of follow-up")+
    ylab("Cumulative incidence (%)")+
    ggtitle(paste("Cumulative hazard:", outcome))
  quartz.save(file = paste(strsplit(path, "CPRD Database")[[1]][1], outcome, "ABCD.jpg"), dpi = 300,width = FigureWidth,height = FigureHeight)
  #ggsave(file = paste(strsplit(path, "CPRD Database")[[1]][1], outcome,"ABCD.jpg"), print(survp),dpi = 1000)
  # Plot cumulative events
  fit <- survfit(surv_object ~ BMI, data = Data)
  survp=ggsurvplot(fit, 
             conf.int = TRUE,
             #palette = c("#E7B800", "#2E9FDF"),
             ggtheme = theme_bw(),
             legend = "bottom", 
             ylim = c(0.0, 0.8),
             legend.title = " ",
             risk.table = TRUE, 
             risk.table.col = "strata",
             fun = "event",)+
    xlab("Year of follow-up")+
    ylab("Cumulative incidence (%)")+
    ggtitle(paste("Cumulative hazard:", outcome))
  quartz.save(file = paste(strsplit(path, "CPRD Database")[[1]][1], outcome, "BMI.jpg"), dpi = 300,width = FigureWidth,height = FigureHeight)
  #ggsave(file = paste(strsplit(path, "CPRD Database")[[1]][1], outcome,"BMI.jpg"), print(survp),dpi = 1000)
  # Plot cumulative events
  fit <- survfit(surv_object ~ Smoking, data = Data)
  survp=ggsurvplot(fit, 
             conf.int = TRUE,
             #palette = c("#E7B800", "#2E9FDF"),
             ggtheme = theme_bw(),
             legend = "bottom", 
             ylim = c(0.0, 0.8),
             legend.title = " ",
             risk.table = TRUE, 
             risk.table.col = "strata",
             fun = "event",)+
    xlab("Year of follow-up")+
    ylab("Cumulative incidence (%)")+
    ggtitle(paste("Cumulative hazard:", outcome))
  quartz.save(file = paste(strsplit(path, "CPRD Database")[[1]][1], outcome, "Smoking.jpg"), dpi = 300,width = FigureWidth,height = FigureHeight)
  #ggsave(file = paste(strsplit(path, "CPRD Database")[[1]][1], outcome,"Smoking.jpg"), print(survp),dpi = 1000)
  # Plot cumulative events
  fit <- survfit(surv_object ~ Gold, data = Data)
  survp=ggsurvplot(fit, 
             conf.int = TRUE,
             #palette = c("#E7B800", "#2E9FDF"),
             ggtheme = theme_bw(),
             legend = "bottom", 
             ylim = c(0.0, 0.8),
             legend.title = " ",
             risk.table = TRUE, 
             risk.table.col = "strata",
             fun = "event",)+
    xlab("Year of follow-up")+
    ylab("Cumulative incidence (%)")+
    ggtitle(paste("Cumulative hazard:", outcome))
  quartz.save(file = paste(strsplit(path, "CPRD Database")[[1]][1], outcome, "Gold.jpg"), dpi = 300,width = FigureWidth,height = FigureHeight)
  #ggsave(file = paste(strsplit(path, "CPRD Database")[[1]][1], outcome,"Gold.jpg"), print(survp),dpi = 1000)
  # Plot cumulative events
  fit <- survfit(surv_object ~ Age, data = Data)
  survp=ggsurvplot(fit, 
                   conf.int = TRUE,
                   #palette = c("#E7B800", "#2E9FDF"),
                   ggtheme = theme_bw(),
                   legend = "bottom", 
                   ylim = c(0.0, 0.8),
                   legend.title = " ",
                   risk.table = TRUE, 
                   risk.table.col = "strata",
                   fun = "event",)+
    xlab("Year of follow-up")+
    ylab("Cumulative incidence (%)")+
    ggtitle(paste("Cumulative hazard:", outcome))
  quartz.save(file = paste(strsplit(path, "CPRD Database")[[1]][1], outcome, "Age.jpg"), dpi = 300,width = FigureWidth,height = FigureHeight)
  #ggsave(file = paste(strsplit(path, "CPRD Database")[[1]][1], outcome,"Age.jpg"), print(survp),dpi = 1000)
}



