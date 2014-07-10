import numpy as np
import pandas as pd

import cond_utils
import beh_utils
import utils

def is_spam(tweet):
    for spam_re in utils.spam_res:
        if spam_re.search(tweet):
            return True
    return False

def get_beh_id(tweet):

    if is_spam(tweet):
        return -1

    if beh_utils.beh_re.search(tweet):
        for id in beh_utils.beh_ids.keys():
            if id in beh_utils.not_words:
                tweet = beh_utils.not_words[id].sub(" ", tweet)
            if beh_utils.in_words[id].search(tweet):
                return id
        pass
    else:
        return -1


def get_cond_id(tweet):

    if is_spam(tweet):
        return -1

    if cond_utils.health_re.search(tweet):
        for id in cond_utils.cond_ids.keys():
            if id in cond_utils.not_words:
                tweet = cond_utils.not_words[id].sub(" ", tweet)
            if cond_utils.in_words[id].search(tweet):
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
