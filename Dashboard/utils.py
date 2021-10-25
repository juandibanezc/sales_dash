import pandas as pd
import math
import time
import datetime as dt
from dateutil.relativedelta import relativedelta

# Time Series of the sales per month
def salesPerMonth(df):
    df_month = df.groupby(['yearMonth']).sum().reset_index(drop=False)
    dff_month = df_month.groupby(['yearMonth']).sum().reset_index(drop=False)
    dff_monthx = dff_month.yearMonth.to_list()

    return dff_monthx

def unixTimeMillis(dt):
    ''' Convert datetime to unix timestamp '''
    return int(time.mktime(dt.timetuple()))

def unixToDatetime(unix):
    ''' Convert unix timestamp to datetime. '''
    return pd.to_datetime(unix,unit='s')

def getMarks(dt, Nth=24):
    ''' Returns the marks for labeling. 
        Every Nth value will be used.
    '''
    result = {}
    for i, date in enumerate(dt):
        # Append value to dict
        result[unixTimeMillis(date)] = str(date.strftime('%Y-%m-%d'))

    return result

def human_format(num):
    magnitude = int(math.log(num, 1000))
    mantissa = str(int(num / (1000**magnitude)))
    return mantissa + ['', 'K', 'M', 'B', 'T', 'P'][magnitude]

def filter_dataframe(df, store_ids, item_levels, item_applications, start_date, end_date):
    
    s = dt.datetime.utcfromtimestamp(start_date).strftime('%Y-%m-%d')
    e = dt.datetime.utcfromtimestamp(end_date).strftime('%Y-%m-%d')

    dff = df[(df['itemApplications'].isin(item_applications))
             & (df['storeID'].isin(store_ids))
             & (df['itemLevel'].isin(item_levels))
             & (df['date'] >= pd.to_datetime(s))
             & (df['date'] <= pd.to_datetime(e))]
    
    return dff

def fetch_aggregate(df):
    sales = df.value.sum()
    customers = df.customerID.nunique()
    tickets = df.ticketNumber.nunique()
    meanTicket = sales/tickets

    return sales, customers, tickets, meanTicket

epoch = dt.datetime.utcfromtimestamp(0)

def get_marks_from_start_end(start, end):
    ''' Returns dict with one item per month
    {1440080188.1900003: '2015-08',
    '''
    result = []
    current = start
    while current <= end:
        result.append(current)
        current += relativedelta(months=1)
    return {unix_time_millis(m):(str(m.strftime('%Y-%m'))) for m in result}

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() #* 1000.0