import numpy as np 

def binnings(items, bins, cache={}):
    if items == 0: 
        return np.zeros((1, bins), dtype=np.int32)
    if bins == 0: 
        return np.empty((0, 0), dtype=np.int32)
    args = (items, bins)
    if args in cache: 
        return cache[args]
    a = binnings(items - 1, bins, cache)
    a1 = a + (np.arange(bins) == 0)
    b = binnings(items, bins - 1, cache)
    b1 = np.hstack((np.zeros((b.shape[0], 1), dtype=np.int32), b))
    result = np.vstack((a1, b1))
    cache[args] = result
    return result