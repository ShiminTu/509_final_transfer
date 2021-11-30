/*
import neighborhood data to big query
*/

from dotenv import load_dotenv
load_dotenv()
import datetime as dt
import pandas as pd
import sqlalchemy as sqa

db = sqa.create_engine('bigquery://musa5092021/final')

neighborhood_column_names = [
    'the_geom',
    'pri_neigh',
    'sec_neigh',
    'shape_area',
    'shape_len',
]
neighborhood = pd.read_csv(f'neighborhood_{dt.date.today()}.csv', names=neighborhood_column_names)
neighborhood.to_sql('neighborhood', db, index=False, if_exists='replace')

