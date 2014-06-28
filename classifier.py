import numpy as np
import pandas as pd

from utils import health_re
from utils import cond_ids
from utils import in_words, not_words

def get_beh_id(tweet):
    return np.random.randint(0, 3)

def get_cond_id(tweet):
    if health_re.search(tweet):
        for id in cond_ids.keys():
            if id in not_words:
                tweet = not_words[id].sub(" ", tweet)
            if in_words[id].search(tweet):
                return id
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
