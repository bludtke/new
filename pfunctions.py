# import libraries
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime

# DEFINE FUNCTIONS


# push dates out of index, cut data down to datetime and opmin
def make_oplist(dataframe):
    dataframe.reset_index(inplace = True)

    oplist = dataframe[['Timestamp', 'Op Min']].values.tolist()
    
    return oplist

# return list of sublists containing all reads with low flow ("off")
def pull_downtimes(op_list, x): 
    return [item for item in op_list if x in item]

# return list of sublists containing only time element (pass in list 
# with elements [date , time, operating min])
def Extract(flaretime):
    return [item[0] for item in flaretime]

# iterates through datetime list to create list of timedelta values
# of time difference between reads
def time_difference(list_time):
    for i in range(len(list_time)):
        return [list_time[i]-list_time[i+1] for list_time[i]
                in list_time if list_time]


# make boolean list if difference greater than two mins
def flag_timejumps(list_timediff):
    twomins = pd.Timedelta(minutes = 2)
    
    list_time_correction = [(i-2) * twomins for i in range(len(list_timediff))]
    
    list_secondsdiff = [list_timediff[i] for i in range(len(list_timediff))]
    
    list_timediff = [list_secondsdiff[i] - list_time_correction[i] for i in range(len(list_secondsdiff))]
    
    check_gap = [list_timediff[i+1] - list_timediff[i] for i in range(len(list_secondsdiff)-1)]
        
    for i in range(len(check_gap)):
        if check_gap[i] > pd.Timedelta(minutes = 0):
            check_gap[i] = 1
        else:
            check_gap[i] = 0
    return check_gap

# make list labeling each downtime with integers 1-n based on time jump bool list
def downtime_jump(list_timejump):
    a = 0
    
    downtime_jump = [a for i in range(len(list_timejump))]
    
    n = 1
    
    for i in range(len(downtime_jump)):
        
        if list_timejump[i-1] == 1:
            
            n = n + 1
            
        downtime_jump[i] = downtime_jump[i] + n
    return downtime_jump


def start_end(downtimes):
    down_list = []

    i = 1
    
    while i in downtimes.index:
        add = pd.DataFrame(downtimes[i])

        down_list.append(add)

        i = i + 1
        
    rangelist = []
    
    for i in range(len(down_list)):
        rangelist.append(down_list[i].head(1))
        rangelist.append(down_list[i].tail(1))

    start_ends = pd.DataFrame(rangelist)

    return start_ends
    
