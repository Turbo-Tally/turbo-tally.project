

def revalue(list_, key, value_map): 

    for item in list_: 
        base = item 
        tokens = key.split(".")

        for token in tokens[:-1]: 
            base = base[token]

        base[tokens[-1]] = value_map[base[tokens[-1]]]
