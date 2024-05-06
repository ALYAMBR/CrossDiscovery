import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data_utils import get_top_k_crossings_originals, get_originals_set
from datasets_list import datasets


def main():
    DATA_DIR_PATH = './data/output/'
    for dataset, target in datasets.items():
        dataset_name = dataset
        data = pd.read_csv(f'{DATA_DIR_PATH}crossed_imp_{dataset_name}_d1.csv')
        data['feature'] = data['Unnamed: 0']
        data = data.drop('Unnamed: 0', axis=1)
        for k in range(1, 11, 1):
            top_k = get_top_k_crossings_originals(data, k=k)
            top_k_originals = get_originals_set(top_k)
            original_features = data[data['rank'].isna()][['feature', 'importance']]
            sorted_original_features = original_features.sort_values(by='importance', ascending=True)
            sorted_original_features.reset_index(drop=True, inplace=True)
            importances_mapping = sorted_original_features.to_dict()['feature']
            inverted_imp_map = {v: k for k, v in importances_mapping.items()}
            top_k_indeces = [inverted_imp_map[feature] for feature in top_k_originals]
            plt.clf()
            ax = sns.barplot(original_features, x='feature', y='importance', color='gray')
            ax.set_title(f'{dataset_name}')
            ax.set_xticks([])
            for ind in top_k_indeces:
                ax.patches[ind].set_facecolor('r')
            plt.savefig(f'./imgs/vis/k{k}/{dataset_name}_k{k}')


if __name__ == '__main__':
    main()