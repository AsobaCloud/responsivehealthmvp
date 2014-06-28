import pandas as pd
import numpy as np
import string
import logging
import classifier
from pandas.io import sql
import MySQLdb

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

def cast_lng_lat(x):
    """
    only for longitude and latitude
    """
    try:
        fx = float(x)
        if np.isnan(fx):
            return 0
        else:
            return int(fx)
    except ValueError:
        logger.warning("Unable to convert %s to int", x)
        return 0

def write_to_db(df, name):
    # TODO: float with nan not being handled

    # HACK:
    sql._SQL_TYPES['text']['mysql'] = 'VARCHAR (255)'

    sql.to_sql(df.where(pd.notnull(df), None), con=con, name=name, flavor='mysql', if_exists='replace', index="id")

def get_zip():
    """
    Get the zip table
    """
    df = pd.read_csv("data/zip_codes_states.csv")
    df = df.rename(columns={"longitude":"lng", "latitude":"lat"})

    for col in ["lng", "lat"]:
        df[col] = df[col].apply(cast_lng_lat)
    write_to_db(df, "zip")
    df = df[["zip_code", "city", "lng", "lat"]]
    return df

def get_sat():
    """
    Get the satisfcation table
    """
    df = pd.read_csv("data/HCAPHS Patient Satisfaction.csv")
    for col in df.columns:
        df[col] = df[col].apply(perc2float)
    sat_col = ["M", "P", "S", "Y", "AB", "AF", "AJ", "AM"]
    sat_col = [col2num(c) for c in sat_col]
    df["sat"] = df[sat_col].apply(calc_sat, axis=1)
    df = df.rename(columns={"ZIP Code":"zip_code"})

    # renaming of columns
    i = 1
    for col in df.columns:
        if "Percent" in col: # renaming only thoes big big percent columns
            df = df.rename(columns={col:i})
            i += 1
    write_to_db(df, "sat")
    df = df[["zip_code", "sat"]]
    return df

def get_tweet():
    """
    Get the tweet table
    NOTE: there are lines with lat == "lat" !!
    """
    df = pd.read_csv("data/tweets.csv", error_bad_lines=False, parse_dates=["created_at"])
    df = df.rename(columns={"lng":"lng"})
    # df = df.dropna(subset=["lng", "lat"]) # TODO: is it right to drop entries without lng, lat?
    for col in ["lat", "lng"]:
        df[col] = df[col].apply(cast_lng_lat)
    df[["beh_id", "cond_id"]] = df["text"].apply(classifier.classify)
    write_to_db(df, "tweet")
    df = df[["text", "lat", "lng", "cond_id", "beh_id"]]
    df = df.dropna()
    return df

def get_res(zip_df, sat_df, tweet_df):
    """
    Get the result table
    """
    tweet_df["count"] = 1
    tweet_df = tweet_df.groupby(["lng", "lat", "cond_id", "beh_id"]).agg({"count":np.sum})
    tweet_df = tweet_df.reset_index()

    sat_df = sat_df.merge(zip_df, on="zip_code")
    sat_df = sat_df.groupby(["lng", "lat"]).agg({"sat":np.average})
    sat_df = sat_df.reset_index()

    res = tweet_df.merge(sat_df, on=["lng", "lat"])
    return res


def main():
    zip_df = get_zip()
    sat_df = get_sat()
    tweet_df = get_tweet()
    res = get_res(zip_df, sat_df, tweet_df)
    write_to_db(res, "result")
    # res = res.dropna()
    print res

if __name__ == "__main__":
    con = MySQLdb.connect(user="root", host="localhost", passwd="sql", db="health")
    main()