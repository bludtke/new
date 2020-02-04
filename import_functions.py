import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime
import glob

# functions to read in excel files

# read flare compiled data (beginn into dataframe
def read_fl278(datafile):
    return pd.read_excel(datafile, skiprows = 25)

def read_fl410(datafile):
    return pd.read_excel(datafile, skiprows = 28)
    
def time_string(flaredata):

    timelist = flaredata['Time'].astype(str)

    del flaredata['Time']
               
    flaredata.insert(1, 'Time', timelist)
    
    return flaredata
    
# replace time and date columns with one column of pd.datetime values
def combine_datetime(flaredata):
    
    date_time_col = flaredata['Date'] + ' ' + flaredata['Time']
    
    date_time_col = pd.Series(date_time_col)
    
    date_time_col = pd.to_datetime(date_time_col, errors = 'ignore', infer_datetime_format = True)
    
    flaredata.insert(0, 'Timestamp', date_time_col)

    del flaredata['Date']
    del flaredata['Time']

    return flaredata

# compile yokogawa files for processing
def read_yoko():
    all_data = pd.read_excel('/Users/benludtke/Documents/working/sensordata/firstfile.xls', index_col = 0)

    for f in glob.glob('/Users/benludtke/Documents/working/sensordata/flaredata*.xls'):
        df = pd.read_excel(f, index_col = 0, skiprows = 27)
    
        n_columns = len(all_data.columns)
    
        columns = all_data.columns
    
        all_data.columns = range(n_columns)
        df.columns = range(n_columns)
    
        all_data = pd.concat([all_data,df], sort = False)
    
        all_data.columns = columns
        
    all_data.to_excel('/Users/benludtke/Documents/working/sensordata/compiled.xlsx', sheet_name = 'SH', header = False, \
                index = True)







