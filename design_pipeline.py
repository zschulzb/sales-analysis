import datetime
import numpy as np
import pandas as pd

lost = 'Lost, Cancelled - 0%'
won = 'Win - 100%'

file_loc = r"C:\Users\Zach_Schulz-Behrend\OneDrive - Dell Technologies\Documents\data\order-oppty_analysis\SFDC pipeline\ZKSB13 - All opportunities-2025-02-25-10-23-06.csv"
file_loc_my_accts = r"c:\Users\Zach_Schulz-Behrend\OneDrive - Dell Technologies\Documents\data\account-alignments\FY26\_myAccounts.xlsx"


def rm_wins_loss(df, state=0):
    # df_oppty_wins = oppty[oppty["Stage"]==won]
    # df_oppty_loses = oppty[oppty["Stage"]==lost]
    # df_oppty_open = oppty[(oppty["Stage"]!=lost) & (oppty["Stage"]!=won)]
    
    if state not in [0,1,2]:
        return "Not valid."
    else:
        if state==0: #rm both
            df = df[df['Stage']!=lost]
            df = df[df['Stage']!=won]
        elif state==1: #rm lost
            df = df[df['Stage']!=lost]
        elif state==2: #rm won
            df = df[df['Stage']!=won]
    
    return df

def revenue_format(df):
    formatted_cols = df['Unweighted Rev'].apply(lambda x: f"${x:,.2f}")
    df['Unweighted Rev Formatted'] = formatted_cols
    cols = df.columns.to_list()
    cols[-1], cols[5] = cols[5], cols[-1]

    return df[cols].sort_values(by=["Unweighted Rev"], ascending=False)

def get_date ():
    curr_date = datetime.datetime.now()

    str_year = str(curr_date.year)

    if curr_date.month < 10:
        str_month = '0' + str(curr_date.month)
    else:
        str_month = str(curr_date.month)

    if curr_date.day < 10:
        str_day = '0' + str(curr_date.day)
    else:
        str_day = str(curr_date.day)


    return str_year + str_month + str_day