import sys
import pandas as pd
import argparse
import os
from sqlalchemy import create_engine
from time import time

def main(params):
    user = params.username
    password = params.password
    host = params.host 
    port = params.port 
    db_name = params.db_name 
    table_name = params.table_name
    url = params.url

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

    # pull zones data, still exists as .csv so no need to unzip
    os.system("wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv")

    zones_df = pd.read_csv('taxi_zone_lookup.csv')
    zones_df.to_sql(name='taxi_zones', con=engine, if_exists='replace')

    # url used here is: "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
    gz_name = 'output.csv.gz'
    csv_name = 'output.csv'

    # get .csv.gz file
    os.system(f"wget {url} -O {gz_name}")
    print('Retrived gz file')
    os.system(f"gzip -d {gz_name}")
    print('Unzipped gz file')


    # initialize taxi table
    df_head = pd.read_csv(csv_name, nrows=1).head(0)

    df_head.to_sql(name=table_name, con=engine, if_exists='replace')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    n = 0

    while True:
        try:
            t_start = time()
            
            df = next(df_iter)

            # just to limit the size while testing
            # df = df.head(100)
            
            df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
            df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
            
            df.to_sql(name=table_name, con=engine, if_exists='append')
            t_end = time()
            
            n += len(df)
            
            print(f"""Inserted {len(df)} values to yellow_taxi_data. 
            This process took {t_end-t_start:.2f} seconds. {n} rows have been inserted in total.""")

        except:
            print('Failed to insert data')
            break

    # needed values to pass
    # user 
    # password 
    # host 
    # port 
    # database name
    # table name
    # csv url

if __name__ == '__main__':
        
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--username', help='Username for Postgres')
    parser.add_argument('--password', help='Password for Postgres')
    parser.add_argument('--host', help='Host for Postgres')
    parser.add_argument('--port', help='Port for Postgres')
    parser.add_argument('--db_name', help='Database name for Postgres')
    parser.add_argument('--table_name', help='Name of the table results will be written to')
    parser.add_argument('--url', help='CSV URL for ingestion into for Postgres')

    args = parser.parse_args()

    main(args)