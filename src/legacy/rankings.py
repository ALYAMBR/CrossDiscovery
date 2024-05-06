import numpy as np

def ranking_average(importances):
    return np.mean(importances)

def ranking_max(importances):
    return np.max(importances)

def ranking_min(importances):
    return np.min(importances)

def ranking_max_minus_min(importances):
    return np.max(importances) - np.min(importances)

def ranking_recursive(importances):
    # TODO recursively sort from top important to less
    pass