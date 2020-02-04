import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime
import glob

def read_fl278(datafile):
    return pd.read_excel(datafile, usecols = [0,1,2,3,4,9], skiprows = 26)

def read_fl4(datafile):
    return pd.read_excel(datafile, usecols = [0,1,2,3,4,9], skiprows = 29)

def read_fl10(datafile):
    return pd.read_excel(datafile, usecols = [0,1,2,3,4], skiprows = 29)

# compile yokogawa files for processing
def read_yoko278(flare,count):
    all_data = pd.read_excel('/Users/benludtke/Documents/working/december/'+ str(flare) + '/firstfile.xls', index_col = 0)

    for f in glob.glob('/Users/benludtke/Documents/working/december/' + str(flare) + '/flaredata*.xls'):
        df = pd.read_excel(f, index_col = 0, skiprows = 27)
    
        n_columns = len(all_data.columns)
    
        columns = all_data.columns
    
        all_data.columns = range(n_columns)
        df.columns = range(n_columns)
    
        all_data = pd.concat([all_data,df], sort = False)
    
        all_data.columns = columns
        
    all_data.to_excel('/Users/benludtke/Documents/working/december/' + str(flare) + '/compiled.xlsx', sheet_name = 'SH', header = False, index = True)
    
def read_yoko410(flare,count):
    all_data = pd.read_excel('/Users/benludtke/Documents/working/december/'+ str(flare) + '/firstfile.xls', index_col = 0)

    for f in glob.glob('/Users/benludtke/Documents/working/december/' + str(flare) + '/flaredata*.xls'):
        df = pd.read_excel(f, index_col = 0, skiprows = 30)
    
        n_columns = len(all_data.columns)
    
        columns = all_data.columns
    
        all_data.columns = range(n_columns)
        df.columns = range(n_columns)
    
        all_data = pd.concat([all_data,df], sort = False)
    
        all_data.columns = columns
        
    all_data.to_excel('/Users/benludtke/Documents/working/december/' + str(flare) + '/compiled.xlsx', sheet_name = 'SH', header = False, index = True)

# split dataframe into list of smaller dataframes of length = size
def list_of_dfs(data, size):

    data_len = len(data)
    count = 0
    df_list = []

    while True:
        if count > data_len-1:
            break

        start = count
        count += size

        df_list.append(data.iloc[start : count])
    return df_list

def get_sh_name(list_of_dfs):
    for i in range(len(list_of_dfs)):
        start = pd.to_datetime(list_of_dfs[i].iloc[[0,2999],[0,1]])
        
# write list of dataframes to excel files named based on start and end timestamp
def write_sh(df_list, timeserieslist, flarenum, undivided_time):
    
    for i in range(len(timeserieslist)):
        
        if (2999 + (i * 3000)) < len(undivided_time):
            starttime = timeserieslist[i][0 + (i * 3000)]
            endtime = timeserieslist[i][2999 + (i * 3000)]
        else:
            starttime = timeserieslist[i][0 + (i * 3000)]
            endtime = timeserieslist[i][len(undivided_time)-1]
        df_list[i].to_excel('/Users/benludtke/Documents/working/december/' + str(flarenum) + '/Flare ' + str(flarenum) + ' ' + starttime + ' thru ' + endtime + '.xlsx', sheet_name = 'SH', header = False , index = False)
        
# replace time and date columns with correct format time stamp
def combine_datetime(flaredata):
    flaredata.reset_index(inplace = True)

    string_time = pd.Series(flaredata.iloc[:, 2].astype(str))

    string_date = pd.Series(flaredata.iloc[:,1])

    list_time = [string_time[i] for i in range(len(string_time))]

    list_date = [string_date[i] for i in range(len(string_date))]

    list_datetime = [list_date[i] + ' ' + list_time[i] for i in range(len(string_date))]
    
    type_datetime = [pd.to_datetime(list_datetime[i]) for i in range(len(list_datetime))]
    
    timestrings = [datetime.datetime.strftime(type_datetime[i],"%m-%d-%Y %H:%M") for i \
                   in range(len(type_datetime))]
    
    return pd.Series(timestrings)

# creates list of series containing timestamp strings for file naming
def list_of_timestrings(timestrings, size):
    list_of_series = [pd.Series(timestrings[i:i+size]) for i in \
                      range(0, len(timestrings), size)]
    return list_of_series
