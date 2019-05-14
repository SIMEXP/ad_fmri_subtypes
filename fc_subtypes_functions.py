import pandas as pd
import numpy as np


def cramers_corrected_stat(confusion_matrix,chi2):
    """ calculate Cramers V statistic for categorial-categorial association.
        uses correction from Bergsma and Wicher, 
        Journal of the Korean Statistical Society 42 (2013): 323-328
    """
    n = confusion_matrix.sum()
    phi2 = chi2/n
    r,k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))    
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2corr / min( (kcorr-1), (rcorr-1)))



#Updates the dataframe to include 2 columns 
#max_subtype - cluster that each subject belongs to 
#max_weight - associated weight with cluster
def max_subtype(dataframe):
    
    max_weight_col = []
    max_subtype_col = []
    weights = []
    
    for column,row in dataframe.iterrows():

        weights = row.tolist()
        weights.pop(0)
        max_weight = max(weights, key=abs)
        max_weight_index = weights.index(max_weight)+1

        max_weight_col.append(max_weight)
        max_subtype_col.append(dataframe.columns[max_weight_index])
    
    dataframe["max_weight"] = max_weight_col
    dataframe["max_subtype"] = max_subtype_col
    
    return dataframe



##Creates a contingency table for given network 
def create_ct(dataframe,num_subtypes):
        
    subtypes_cols_ct = list(dataframe.columns[1:num_subtypes+1])
    cols_ct =  ["class"] + subtypes_cols_ct
    contingency_table = pd.DataFrame(columns = cols_ct)
    contingency_table["class"] = ["CN","ADMCI"]    
    
    

    for subtype_ct in subtypes_cols_ct:

        class_sum_cn = dataframe.loc[dataframe["max_subtype"] == subtype_ct]["CN"].sum()
        contingency_table.loc[contingency_table["class"] == "CN", [subtype_ct]] = class_sum_cn
       
        class_sum_admci = dataframe.loc[dataframe["max_subtype"] == subtype_ct]["AD"].sum()
        class_sum_admci += dataframe.loc[dataframe["max_subtype"] == subtype_ct]["MCI"].sum()
       #class_sum_admci += dataframe.loc[dataframe["max_subtype"] == subtype_ct]["SCI"].sum()
        contingency_table.loc[contingency_table["class"] == "ADMCI", [subtype_ct]] = class_sum_admci

    
    return contingency_table
    
    
    
    
