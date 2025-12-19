def sumdva(numbs, target):
    if (type(target) == int) and (type(numbs) == list) and (len(numbs) > 1):
        if all(type(numbs[i]) == int for i in range(0, len(numbs))):
            for i in range(0, len(numbs)):
                for j in range(i + 1, len(numbs)):
                    if numbs[i] + numbs[j] == target:
                        return [i, j]
    

