#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 18:28:36 2020

@author: babaniyi

a rather simple ETL process from API data retrieved using Requests, its manipulation in Pandas, and the 
eventual write of that data into a database (BigQuery). The dataset we’ll be analyzing and importing is 
the real-time data feed from Citi Bike in NYC. The data is updated regularly (every few seconds) and can 
be accessed from the Citi Bike System Data feeds.

"""
import os
os.chdir('/Users/babaniyi/Documents/Babaniyi/learn/Blessing')

#Set Up the ETL Environment
###API & Pandas Requirements

import requests # import data from .json feed
import pandas as pd 
import sys # stop pythin from running when a criteria is met
from pandas.io.json import json_normalize # transform .json object to dataframe
from datetime import datetime
import gc   #clean  memory footprint



# BIGQUERY _________________________
###Database Connection Details
### Detailed info on connecting to BigQuery: https://cloud.google.com/bigquery/docs/pandas-gbq-migration
#
full_table_id = 'XXXXXXXXXXX'
#
project_id = 'XXXXXXXXXXX'



q_check_contents = """SELECT max(last_system_update_date) as last_system_update_date FROM testproject_213618.citibike_data"""
#_____________________________________________________________________

# SQL Database Connection Details____________________________________

user = 'XXXX'
host = 'XXXX'
port = 'XXXX'
password = 'XXXX'
database_name = 'XXXX'

'''
postgresql://[user[:password]@][host][:port]
"postgresql://repl:password@localhost:5432/pagila" ---- sample format

'''
import sqlalchemy
connection_uri = "postgresql://user:password@host:port/database_name"
db_engine = sqlalchemy.create_engine(connection_uri)
#_____________________________________________________________________






#_______ EXTRACT_____________
def request_data(url):
    '''
    Function to extract data from API

    Parameters
    ----------
    url : TYPE url
        url of API

    Returns
    -------
    r : TYPE json
        Extracted json file from API

    '''
    r = requests.get(url)
    if r.status_code != 200:
        print("Data Source Server Status Issue ")
        gc.collect()
        sys.exit()
    else:
        print("Server Status Shows New Update ")
        pass
    return r

#______________ TRANSFORM_____________
def construct_dataframe(r):
    '''
    Function to create a dataframe extracting, station names, time updated 
    Parameters
    ----------
    r : TYPE object
        get web server
        

    Returns
    -------
    df : TYPE dataframe
        Dataframe containing data extracted from the API

    '''
    stations = r.json()['data']['stations']
    last_updated = r.json()['last_updated']

    dt_object = datetime.fromtimestamp(last_updated).strftime('%Y-%m-%d %H:%M:%S')
    print("Last Updated: " + str(dt_object))

    df = json_normalize(stations)
    df['last_system_update_date'] = dt_object
    df['insertion_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\nData For Insertion Constructed ")
    return df


#___________________ LOADING_____________
def insert_data(df, export):
    '''
    Function to export data to sql, bigquery, csv
    Parameters
    ----------
    df : TYPE - dataframe
        dataframe derived from the Bike sharing API
    export : TYPE - string
        it should either be bigquery or sql

    Returns
    -------
    None.
    Exports data to selected format

    '''
    if export == 'sql':
        pd.to_sql(df, db_engine)
        print("\nSQL Data Insertion Time: " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
    elif export == 'bigquery':
        df.to_gbq(full_table_id, project_id=project_id,if_exists='append')
        print("\nBigQuery Data Insertion Time: " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
    elif export == 'csv':
        df.to_csv("citibike_stations_data.csv")
        print("\nCSV Data Insertion Time: " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
    else:
        print("The format you requested is not available, please select one of the 3 below: \nsql \nbigquery \ncsv")

    return




'''
Building Data Quality Tests
One last step we perform in the ETL is to ensure that on runs of the ETL we don’t have duplicative records 
entered into the database. This can often happen with basic runs of an ETL due to several upstream reasons
 in our API data. In this case, we constantly check to see whether the system update date in the database
 is less than the last date pulled from the API. This helps prevent us having duplicative records by only 
 allowing new data to flow through the ETL if there is for some reason a slow-down in the upstream 
 Citi Bike API.
'''

#__________________ DATA QUALITY TESTS_______________
def check_contents(r,df,mq_check_contents=q_check_contents,project_id=project_id):
    d = pd.read_gbq(q_check_contents,project_id=project_id)
    #last system update record in the database
    last_system_update_date = d['last_system_update_date'][0]
    #last system update reported by the server response
    last_updated = datetime.fromtimestamp(r.json()['last_updated']).strftime('%Y-%m-%d %H:%M:%S')
    #check if the last_system_update_date entered in the database is less than the current date.
    #if it is not, do not insert the new data as you'll be adding duplicative records
    if last_system_update_date > last_updated:
        print("\nData not inserted due to duplicative records ")
        gc.collect()
        sys.exit()
    else:
        print("\nData does not contain duplicate records ")
        insert_data(df)
    return


url = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"

r = request_data(url) 
df = construct_dataframe(r)
   
## Below function to be run only once on the first insertion of data into the new table
insert_data(df, 'java')
#check_contents(r,df)
#gc.collect()





