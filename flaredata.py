
# import libraries
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime
from datetime import date

# import functions
from pfunctions import low_flow, operating_minutes, pull_downtimes, \
    time_type, time_difference, make_oplist, flag_timejumps, downtime_jump

from import_functions import read_fl10

# read file
df = read_fl10('/Users/benludtke/Documents/working/flaredata.xlsx')
                   
# OP MIN AND TOT FLOW

# create two series of flow values for operating minutes and total flow
flow = df.iloc[:, 3]

flowvals = flow

# create operating minutes series based on flow values
flow.apply(low_flow)

opmin = flow.apply(operating_minutes)

# create total flow series with operating minutes and flow values
totflow = pd.Series.multiply(flowvals, opmin)

# insert operating minutes and total flow series into dataframe
df.insert(4, 'Op Min', opmin)

df.insert(5, 'Total Flow', totflow)

# PULL DOWNTIMES

# make operating list ([date, time, op min])
op_list = make_oplist(df)

# filter for downtime reads
downtimes = pull_downtimes(op_list,0)

# make list of pd.datetime time values
timevaldown = time_type(downtimes)

# make list of pd.timedelta time difference values
difference = time_difference(timevaldown)

# make boolean series to flag date jumps in downtimes
list_timejump = flag_timejumps(difference)

# make integer list to categorize downtimes
downtime_list = downtime_jump(list_timejump)

# drop last row for calculations
downtimes.pop()

# make series
series_downtimes = pd.Series(downtimes)

# categorize index
series_downtimes.index = downtime_list

# create dataframe with organized indices
df_downtimes = pd.DataFrame(series_downtimes)

df_downtimes.to_excel('/Users/benludtke/Documents/working/downtimes.xlsx', sheet_name = 'Downtimes')

df.to_excel('/Users/benludtke/Documents/working/processed_data.xlsx', sheet_name = 'Flow Data')

