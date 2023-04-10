
def get_top_k_crossings_originals(crossings, k=5):
    crossings = crossings.sort_values(by='importance', ascending=False).dropna()
    top_k = crossings[0:k]
    return top_k

def get_originals_set(crossings):
    uniq_vals_lists = crossings['feature'].unique().tolist()
    uniq_vals = []
    for val in uniq_vals_lists:
        uniq_vals += val.split('_X_')
    return list(set(uniq_vals))