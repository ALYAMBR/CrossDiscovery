import collections

def remove_duplicates(crossings_list):
    uniq_crossings = []
    for crossing in crossings_list:
        if crossing not in uniq_crossings:
            uniq_crossings.append(crossing)
    return uniq_crossings
    
def build_crossings_prototypes(data, depth):
    columns = data.columns
    crossings = [[col] for col in columns]
    for _ in range(depth):
        crossings = remove_duplicates([sorted(old_cross + [column]) for old_cross in crossings for column in columns])
    prototypes = remove_duplicates(crossings)
    return prototypes

def _get_crossing_name(crossing):
    crossing_name = '_X_'.join(crossing)
    return crossing_name

def build_crossings(data, crossings, cross_function):
    for crossing in crossings:
        cross_name = _get_crossing_name(crossing)
        data[cross_name] = cross_function(data, crossing)
    return data