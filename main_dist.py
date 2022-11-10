import pandas as pd
import numpy as np
import scipy
from scipy import stats
import distribution_calc as dc

#File to be processed
datafile = 'H2S_data_parsed.xlsx'

#Filename of result document
Result_filename = datafile.split(".")[0] + "_Results_pygen.xlsx"

#Imports dataframe and gets list of Data set IDs
data_df=pd.read_excel(datafile,sheet_name=0)
IDlist = data_df.columns.values
IDlist = IDlist[1:]

#Defines dictionaries
data_df_collection = {} 
dataset_size_collection = {}

#Sets labels
Property_list_labels= ['Name of stream/PL','Dataset Size','Distribution/chi_square']
Property_list_labels_df = pd.DataFrame(Property_list_labels)

#Loops through ID list
for ID in IDlist:
    jj=+1

    #calculates the distibution ranking and adds it to dictionary
    data_df_collection[ID] = dc.column_calc(datafile,ID)

    #calculates size of data set and adds it to dictionary
    datasetsize = [len(data_df[ID].dropna())]
    dataset_size_collection[ID] = pd.DataFrame(datasetsize)

#Writes to "Result_filename".xlsx
with pd.ExcelWriter(Result_filename) as writer:

    #Adds labels to excel
    Property_list_labels_df.to_excel(writer,startrow = 0, startcol = 0,index=False,header = False)
    ii = 1
    
    for ID in IDlist:

        #Adds ID name to top of column in excel
        IDdf = pd.DataFrame([ID])
        IDdf.to_excel(writer,startrow = 0, startcol = ii,index=False,header = False)

        #Adds dataset size next in the column in excel
        dataset_size_collection[ID].to_excel(writer,startrow = 1, startcol = ii,index=False,header = False)

        #Adds dataset results next in the column in excel
        data_df_collection[ID].to_excel(writer,startrow = 2, startcol = ii,index=False,header = False)
        ii = ii + 2
