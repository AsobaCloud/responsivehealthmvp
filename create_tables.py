import pandas as pd
from pandas.io import sql


from pandas.io import sql
import MySQLdb

con = MySQLdb.connect(user="root", passwd="sql", db="health", host="localhost")

def create_zip():
    fname = "data/zip_codes_states.csv"
    df = pd.read_csv(fname)
    sql.write_frame(df, con=con, name='zip',
                if_exists='replace', flavor='mysql')


if __name__ == "__main__":
    create_zip()