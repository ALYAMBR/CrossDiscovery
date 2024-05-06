import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from data_utils import get_target
from datasets_list import datasets
from CrossingBuilder import build_crossings, build_crossings_prototypes
from crossing_functions import crossing_product
from importances import get_point_biserial_corrs

def main(depth=1):
    DATA_DIR_PATH = './data/'
    for dataset, target in datasets.items():
        DATASET_NAME = dataset
        data = pd.read_csv(f'{DATA_DIR_PATH}{DATASET_NAME}.csv')
        data = data.dropna(axis=0)
        target_col = data[target]
        if target_col.dtype not in ['float64', 'int64']:
            label_ecnoder = LabelEncoder()
            target_col = label_ecnoder.fit_transform(target_col)
        data = data.drop(target, axis=1)
        data = data.select_dtypes(include=['float64', 'int64'])
        # feat_cols = data.columns
        data['target'] = target_col
        prototypes = build_crossings_prototypes(data.drop(['target'], axis=1), depth)
        orig_imp = get_point_biserial_corrs(data, 'target')
        crossed_data, cross_info = build_crossings(data, prototypes, crossing_product, orig_imp)
        crossed_imp = abs(crossed_data.corr()['target']).sort_values()
        crossed_full_info = pd.DataFrame(crossed_imp)
        crossed_full_info['importance'] = crossed_full_info['target']
        crossed_full_info = crossed_full_info.drop('target', axis=1)
        crossed_full_info['rank'] = pd.Series(dict({k: v[0] for k, v in cross_info.items()}))
        crossed_full_info['originals'] = pd.Series(dict({k: v[1] for k, v in cross_info.items()}))
        crossed_full_info = crossed_full_info.drop('target', axis=0)
        crossed_full_info.to_csv(f'./data/output/crossed_imp_{DATASET_NAME}_d{depth}.csv')
        pd.DataFrame(orig_imp, columns=['importance']).to_csv(f'./data/output/orig_imp_{DATASET_NAME}.csv', index=True)

if __name__ == '__main__':
    main(depth=1)