import numpy as np
import pandas as pd

def get_beh_id(tweet):
    return np.random.randint(0, 10)

def get_cond_id(tweet):
    return np.random.randint(0, 10)

def classify(tweet):
    beh_id = get_beh_id(tweet)
    cond_id = get_cond_id(tweet)

    return pd.Series([beh_id, cond_id])
