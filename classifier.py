import numpy as np
import pandas as pd

cond_dict = {
                "Mental":0,
                "Infectious Disease":1,
                "Cardiovascular":2,
                "Colorectal":3,
                "Respiratory":4,
                "Injury":5,
                "Skin":6,
                "Neonatal":7,
                "Blood Disorder":8,
                "Drug":9
              }

def get_beh_id(tweet):
    return np.random.randint(0, 3)

def get_cond_id(tweet):
    return np.random.randint(0, 3)

def classify(tweet):
    beh_id = get_beh_id(tweet)
    cond_id = get_cond_id(tweet)

    return pd.Series([beh_id, cond_id])
