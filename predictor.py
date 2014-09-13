'''
Created on Jul 19, 2014

@author: shah
'''

from __future__ import division

import glob
import json
import os
import pandas as pd
from process_data import cast_lng_lat

ZIP_DICT = None
ZIP_DF = None
HCUPNET = None
BEH_DF = None

def load_zip(zip_dict):
    """
    Get the zip table
    """
    df = pd.read_csv("data/zip_codes_states.csv")
    df = df[["zip_code", "longitude", "latitude", "state", "county", "city"]]
    df = df.rename(columns={"longitude":"lng", "latitude":"lat"})

    for col in ["lng", "lat"]:
        df[col] = df[col].apply(cast_lng_lat)

    mask = df["zip_code"].isin(zip_dict)
    return df[mask]

def get_sc(zip_code):
    mask = ZIP_DF['zip_code'] == zip_code
    state = ZIP_DF[mask]['state'].values[0]
    county = ZIP_DF[mask]['county'].values[0]
    return state, county

def load_zip_dict():
    """
    load the zip population dict
    """
    df = pd.read_csv("data/zip_pop.csv")
    df['sex_0'] = df["sex_pct_male"]
    df['sex_1'] = df["sex_pct_female"]

    df['age_0'] = df["age_pct_0_19"] * (1 / 20) # <1
    df['age_1'] = df["age_pct_0_19"] * (17 / 20) # 1-17
    df['age_2'] = df["age_pct_0_19"] * (2 / 20) + df["age_pct_20_39"] + df["age_pct_40_59"] * (4 / 20) # 18-44
    df['age_3'] = df["age_pct_40_59"] * (16 / 20) + df["age_pct_60_79"] * (5 / 20) # 44-65
    df['age_4'] = df["age_pct_60_79"] * (15 / 20) + df["age_pct_80_over"] # 65+

    columns = ["zip", "population", "sex_0", "sex_1", "age_0", "age_1", "age_2", "age_3", "age_4"]
    df = df[columns]
    df = df.set_index("zip")
    t_dict = json.loads(df.to_json(orient="index"))
    zip_dict = {}

    for zip_code in t_dict:
        zip_dict[int(zip_code)] = t_dict[zip_code]

    return zip_dict

def get_beh_ratio(beh_id, zip_code):
    # get lng, lat
    mask = ZIP_DF["zip_code"] == zip_code

    lat = ZIP_DF[mask]['lat'].values[0]
    lng = ZIP_DF[mask]['lng'].values[0]

    # get count
    mask = (BEH_DF["lng"] == lng) & (BEH_DF["lat"] == lat) & (BEH_DF["beh_id"] == beh_id)
    count = len(BEH_DF[mask]["screen_name"].unique())

    # total length
    mask = (BEH_DF["lng"] == lng) & (BEH_DF["lat"] == lat)
    total_count = len(BEH_DF[mask]["screen_name"].unique())

    if total_count != 0:
        beh_ratio = count / total_count
    else:
        print "Warning, No data for %s, %s" % (lng, lat)
        beh_ratio = 0.1

    return beh_ratio


def get_pop_ratio(zips, zip_code):
    """
    return ration of pop(zip) / pop(zips)
    """
    total = 0
    for z in zips:
        try:
            total += ZIP_DICT[z]["population"]
        except:
            pass

    return 1. * ZIP_DICT[zip_code]["population"] / total

def get_zips(county, state):
    """
    return all the zip codes in the county
    """
    mask = (ZIP_DF["county"] == county) & (ZIP_DF["state"] == state)
    return ZIP_DF[mask]["zip_code"].values

def get_zips_by_city(zip_df, city):
    mask = (zip_df["city"] == city)
    zips = zip_df[mask]["zip_code"].values
    return zips

def load_hcupnet():
    hcupnet = {}
    for file in glob.glob("data/hcupnet/*.json"):
        name = os.path.basename(file).split(".")[0]
        state, county = name.split("_")
        data = json.load(open(file))

        if not state in hcupnet:
            hcupnet[state] = {}

        hcupnet[state][county] = data

    return hcupnet

def load_data():
    global ZIP_DICT, ZIP_DF, HCUPNET, BEH_DF
    ZIP_DICT = load_zip_dict()
    ZIP_DF = load_zip(ZIP_DICT)
    BEH_DF = pd.read_csv("data/beh_df.csv")
    HCUPNET = load_hcupnet()
    print "Data Loaded"

def predict(sex, age, beh_id, zip_code):
    global ZIP_DICT, ZIP_DF, HCUPNET

    if ZIP_DICT is None or ZIP_DF is None or HCUPNET is None:
        load_data()

    if zip_code not in ZIP_DICT:
        return {"Error":"Zip not found"}

    state, county = get_sc(zip_code)
    zips = get_zips(county, state)
    pop_ratio = get_pop_ratio(zips, zip_code)
    data = HCUPNET[state][county]

    age_key = "age_%s" % age
    sex_key = "sex_%s" % sex

    # beh_ratio = beh_utils.counts[beh_id] / sum(beh_utils.counts.values()) # * (ZIP_DICT[zip_code][age_key] / 100) * (ZIP_DICT[zip_code][sex_key] / 100)
    beh_ratio = get_beh_ratio(beh_id, zip_code)

    # sex_ratio = data["total_discharge"]["sex"][sex] / sum(data["total_discharge"]["sex"].values())
    sex_ratio = ZIP_DICT[zip_code][sex_key] / 100

    adm = data["total_discharge"]["age_group"][age] * pop_ratio * sex_ratio * beh_ratio
    stay = data["mean_stay"]["age_group"][age] * adm
    cost = data["cost"]["age_group"][age] * adm

    if adm == 0:
        pass

    ans = {
           "Expected Admissions": adm,
           "Expected Stay": stay,
           "Expected Cost": cost,
           "Expected Stay per person": data["mean_stay"]["age_group"][age],
           "Expected Cost per person": data["cost"]["age_group"][age],

           }

    return ans

def predict_by_cities(sex, age, beh_id, cities):
    if ZIP_DF is None:
        load_data()
    results = {}
    cities = cities.split(",")
    for city in cities:
        city = city.strip()
        results[city] = {}
        zips = get_zips_by_city(ZIP_DF, city)
        for z in zips:
            try:
                results[city][str(z)] = predict(sex, age, beh_id, z)
            except Exception as e:
                print "ERROR"
    return results

def _test():
    print predict('0', '1', 7, 90001)
    print predict('1', '1', 7, 90001)
    print predict_by_cities('1', '1', 7, u"Oakland")

def main():
    _test()

if __name__ == '__main__':
    main()
