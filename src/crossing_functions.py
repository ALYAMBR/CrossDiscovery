def crossing_product(data, crossing):
    result = data[crossing[0]]
    for feature in crossing[1:]:
        result *= data[feature]
    return result