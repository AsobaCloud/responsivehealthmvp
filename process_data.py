import pandas as pd
import numpy as np
import string
import logging
import classifier

logger = logging.getLogger(__name__)
logging.basicConfig()

def calc_sat(row):
    """
    Calcualte the satisfaction metrics
    """
    val = row.values
    sat = np.mean(val)
    return sat

def perc2float(x):
    if type(x) == str and x[-1] == "%":
        return float(x[:-1])
    else:
        return x

def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num - 1

def cast_long_lat(x):
    """
    only for longitude and latitude
    """
    try:
        fx = float(x)
        if np.isnan(fx):
            return np.nan
        else:
            return int(fx)
    except ValueError:
        logger.warning("Unable to convert %s to float", x)
        return np.nan


def get_zip():
    df = pd.read_csv("data/zip_codes_states.csv")
    df = df[["zip_code", "city", "longitude", "latitude"]]
    df = df.rename(columns={"longitude":"long", "latitude":"lat"})

    for col in ["long", "lat"]:
        df[col] = df[col].apply(cast_long_lat)
    return df

def get_sat():
    df = pd.read_csv("data/HCAPHS Patient Satisfaction.csv")
    for col in df.columns:
        df[col] = df[col].apply(perc2float)
    sat_col = ["M", "P", "S", "Y", "AB", "AF", "AJ", "AM"]
    sat_col = [col2num(c) for c in sat_col]
    df["sat"] = df[sat_col].apply(calc_sat, axis=1)
    df = df.rename(columns={"ZIP Code":"zip_code"})
    df = df[["zip_code", "sat"]]
    return df

def get_tweet():
    """
    NOTE: there are lines with lat == "lat" !!
    """
    df = pd.read_csv("data/tweets.csv")
    df = df.rename(columns={"lng":"long"})
    df = df.dropna(subset=["long", "lat"]) # TODO: is it right to drop entries without long, lat?
    for col in ["lat", "long"]:
        df[col] = df[col].apply(cast_long_lat)
    df = df[["text", "lat", "long"]]
    df[["beh_id", "cond_id"]] = df["text"].apply(classifier.classify)
    return df

def get_res(zip_df, sat_df, tweet_df):
    tweet_df["count"] = 1
    tweet_df = tweet_df.groupby(["long", "lat", "cond_id", "beh_id"]).agg({"count":np.sum})
    tweet_df = tweet_df.reset_index()

    sat_df = sat_df.merge(zip_df, on="zip_code")
    sat_df = sat_df.groupby(["long", "lat"]).agg({"sat":np.average})
    sat_df = sat_df.reset_index()

    res = tweet_df.merge(sat_df, on=["long", "lat"])
    return res


def main():
    zip_df = get_zip()
    sat_df = get_sat()
    tweet_df = get_tweet()
    res = get_res(zip_df, sat_df, tweet_df)
    print res

if __name__ == "__main__":
    main()