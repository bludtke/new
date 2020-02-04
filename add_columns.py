import pandas as pd

# change all "off" flow values to zero
def low_flow(flow):
    if flow < 10:
        
        flow = 0
    return flow

# change all "on" flow values to two (for operating minutes)
def operating_minutes(flow):
    if flow > 10:
        
        flow = 2
        
    else:
        
        flow = 0
    return flow

# transform two flow series' into operating minutes and total flow columns
def add_cols(dataframe):
    flow = dataframe['SCFM']

    flow2 = flow

    flow.apply(low_flow)

    opmin = flow.apply(operating_minutes)

    totflow = pd.Series.multiply(flow2, opmin)

    dataframe.insert(4, 'Op Min', opmin)

    dataframe.insert(5, 'Total Flow', totflow)

    return dataframe

# return summary dataframe to push to excel
def summary_table(dataframe):
    opmin = dataframe['Op Min']
    flows = dataframe['Total Flow']

    totalmin = opmin.sum()
    
    totalhrs = totalmin / 60
    totalflow = flows.sum()
    avgflow = totalflow / totalmin
    mininmonth = 44640
    avgmonth = totalflow / mininmonth

    summary = pd.Series([totalmin, totalhrs, totalflow, avgflow, mininmonth,\
                         avgmonth])

    sumindex = ['Total Operating Minutes', 'Total Operating Hours', 'Total Flow',\
                    'Average Flow', 'Minutes in Month', 'Monthly Average Flow']

    summary.index = sumindex

    summary = pd.DataFrame(summary)

    return summary

