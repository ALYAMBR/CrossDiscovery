from scipy.stats import pointbiserialr as pcorr
import pandas as pd

def get_point_biserial_corrs(data, target):
    columns = data.drop(target, axis=1).columns
    pcorrs_orig = dict()
    for col in columns:
        pcorrs_orig.update({col:abs(pcorr(data[col], data[target])[0])})
    return pd.Series(pcorrs_orig).sort_values()