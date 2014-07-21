'''
Created on Jul 19, 2014

@author: shah
'''

from __future__ import division

import glob
import json
import os
import pandas as pd

def load_zip():
    """
    Get the zip table
    """
    df = pd.read_csv("data/zip_codes_states.csv")
    df = df[["zip_code", "state", "county"]]
    return df

def get_sc(zip_df, zip_code):
    mask = zip_df['zip_code'] == zip_code
    state = zip_df[mask]['state'].values[0]
    county = zip_df[mask]['county'].values[0]
    return state, county

def load_zp_dict():
    """
    load the zip population dict
    """
    df = pd.read_csv("data/zip_pop.csv")
    df = df[["zip", "population"]]
    df = df.set_index("zip")
    t_dict = json.loads(df.to_json())['population']
    zp_dict = {}

    for zip in t_dict:
        zp_dict[int(zip)] = t_dict[zip]

    return zp_dict

def get_pop_ratio(zp_dict, zips, zip_code):
    """
    return ration of pop(zip) / pop(zips)
    """
    total = 0
    for z in zips:
        try:
            total += zp_dict[z]
        except:
            pass

    return 1. * zp_dict[zip_code] / total

def get_zips(zip_df, county, state):
    """
    return all the zip codes in the county
    """
    mask = (zip_df["county"] == county) & (zip_df["state"] == state)
    return zip_df[mask]["zip_code"].values

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

def create_model():
    pass

ZIP_DF = load_zip()
ZP_DICT = load_zp_dict()
HCUPNET = load_hcupnet()
def predict(sex, age, beh_id, zip_code):

    state, county = get_sc(ZIP_DF, zip_code)
    zips = get_zips(ZIP_DF, county, state)
    pop_ratio = get_pop_ratio(ZP_DICT, zips, zip_code)

    data = HCUPNET[state][county]

    sex_ratio = data["total_discharge"]["sex"][sex] / sum(data["total_discharge"]["sex"].values())
    adm = data["total_discharge"]["age_group"][age] * pop_ratio * sex_ratio

    stay = data["mean_stay"]["age_group"][age] * adm
    cost = data["mean_stay"]["age_group"][age] * stay

    ans = {
           "Expected Admissions": adm,
           "Expected Stay": stay,
           "Expected Cost:": cost
           }

    return ans


def _test():
    print predict('0', '1', '2', 60004)
    print predict('0', '1', '2', 60005)

def main():
    _test()

if __name__ == '__main__':
    main()