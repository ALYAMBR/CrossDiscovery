import collections
def remove_duplicates(crossings_list):
    uniq_crossings = []
    for crossing in crossings_list:
        if crossing not in uniq_crossings:
            uniq_crossings.append(crossing)
    return uniq_crossings
    

def _build_crossing_prototypes(columns, depth):
    crossings = [[col] for col in columns]
    for _ in range(depth):
        crossings = [sorted(old_cross + [column]) for old_cross in crossings for column in columns]
    result = remove_duplicates(crossings)
    return result

def build_crossings(data, cross_function, depth):
    columns = data.columns
