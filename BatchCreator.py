#GetBatches function
#Returns a list of batches of size batch_size with parameters of choice from .csv files
#in form of numpy arrays. The list has shape [numBatches,BatchSize,NumParameters] while
#NumBatches = minLen(inputFiles)/BatchSize. It returns two of those lists, one for input
#and one for the corresponding labels. Data needs to be present in .csv form.

#Parameter:
#IncsvFiles - list of csv file names from which data should be extracted for input
#InVariableNames - Names of columns of csv files which should be used as input (list of lists for each csv)
#OutcsvFiles - list of csv file names from which data should be extracted as targets
#OutVariableNames - Names of columns of csv files which should be used as target (list of lists for each csv)
#BatchSize - how many samples are in each batch

#Output:
#Batch: List of input variables
#Label: List of target variables

#Import dependencies
#from src.setup.config import db
#from itertools import groupby
import pandas as pd
#from collections import OrderedDict
#from datetime import date
import numpy as np
#import pyodbc

def GetBatches(IncsvFiles,InVariableNames,OutcsvFiles,OutVariableNames,BatchSize):
    counter = 0
    MinFileLen = 10000000000000
    Batches = []
    Labels = []
    while counter<MinFileLen-BatchSize:
        Batch = []
        Label = []
        print(counter)
        for n,Infile in enumerate(IncsvFiles):
            file = pd.read_csv(str(Infile))
            if len(file)<MinFileLen:
                MinFileLen = len(file)
                print("len: "+str(MinFileLen))
            for variable in InVariableNames[n]:
                variableValues = []
                for e in range(BatchSize):
                    value = file[variable].iloc[counter+e]
                    variableValues.append(value)
                Batch.append(variableValues)
        for n,Outfile in enumerate(OutcsvFiles):
            file = pd.read_csv(str(Outfile))
            for variable in OutVariableNames[n]:
                variableValues = []
                for e in range(BatchSize):
                    value = file[variable].iloc[counter+e]
                    variableValues.append(value)
                Label.append(variableValues)
        counter = counter+BatchSize
        Batches.append(Batch)
        Labels.append(Label)
    return Batches,Labels

#Example use:
b,l = GetBatches(['ICDList.csv','OPSList.csv'],[['ID2','ICDs'],['OPSs']],['OPSList.csv'],[['ID']],100)
#In this case we extract two variables (ID2 and ICDs) from the ICDList.csv file and one variable (OPSs)
#from the OPSList.csv file for the input of the network. For the output we extract ID from OPSList.csv.
#Our two lists are of size 12600 such that we get 126 batches with a batch size of 100. This means that
# b has shape [126,100,3] and l has shape [126,100,1]
