#!/usr/bin/env python
# coding: utf-8

# In[3]:


# import libraries
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime

# import functions
from sh_functions import read_fl278, list_of_dfs, write_sh, combine_datetime, list_of_timestrings


# In[4]:


# read file (flares 2, 7, 8)
df = read_fl278('/Users/benludtke/Documents/working/flaredata2.xlsx')

# make list of timestamp strings to use for naming
timestamp_series = combine_datetime(df)

# break list up into 3000 row chunks to use for naming
timeserieslist = list_of_timestrings(timestamp_series, 3000)

# delete extra index column
del df['index']

# split flare data up into list of 3000 row dataframes
df_list = list_of_dfs(df, 3000)

# write into excel files
write_sh(df_list, timeserieslist, 2, timestamp_series)

