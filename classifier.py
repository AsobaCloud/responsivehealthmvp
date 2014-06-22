import re

import numpy as np
import pandas as pd


cond_dict = {
                "mental":0,
                "infectious":1,
                "cardiovascular":2,
                "colorectal":3,
                "respiratory":4,
                "injury":5,
                "skin":6,
                "neonatal":7,
                "blood":8,
                "drug":9,
                "others":10
              }

health_words = ["disease", "disorder", "illness", "condition",
          "health", "medicine", "fitness"]

health_re = re.compile("|".join(health_words))

def get_beh_id(tweet):
    return np.random.randint(0, 3)

def get_cond_id(tweet):
    if health_re.search(tweet):
        for cond in cond_dict.keys():
            if cond in tweet:
                return cond_dict[cond]
        return cond_dict["others"]
    else:
        return -1

def clean_tweet(t):
    t = t.lower()
    return t

def classify(tweet):
    tweet = clean_tweet(tweet)
    beh_id = get_beh_id(tweet)
    cond_id = get_cond_id(tweet)

    return pd.Series([beh_id, cond_id])
