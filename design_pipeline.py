import datetime
import numpy as np
import pandas as pd


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

def add_acct_alignments(df1, df2):
   df3 = df1.index.to_series().apply(lambda x: df2[df2.index==x].loc[x,'SE':'Region'])
   return pd.concat([df1, df3], axis=1)

lost = 'Lost, Cancelled - 0%'
won = 'Win - 100%'

date = get_date()

file_loc = r"C:\Users\Zach_Schulz-Behrend\data\order-oppty_analysis\SFDC pipeline\ZKSB13 - All opportunities-2025-02-25-10-23-06.csv"
file_loc_my_accts = r"c:\Users\Zach_Schulz-Behrend\data\account-alignments\FY26\_myAccounts.xlsx"
file_loc_store_designs = r"c:\Users\Zach_Schulz-Behrend\data\order-oppty_analysis\Designs_{0}.xlsx".format(date)
out_cols = ['Account Name', 'SE', 'AE', 'ISR', 'Region', 'Opportunity Name', 'Stage', 'Unweighted Rev',
            'Unweighted Rev Currency', 'Probability (%)', 'Age','Book Date', 'Created Date', 'Next Step', 
            'Opportunity Type',]

if __name__ == '__main__':
    oppty = pd.read_csv(file_loc)
    oppty = rm_wins_loss(df=oppty)

    df_my_accts = pd.read_excel(file_loc_my_accts, sheet_name="Account Search Result", nrows=68, usecols="A:B, D:G")
    df_my_accts = df_my_accts.set_index(df_my_accts.ID)
    df_my_accts = df_my_accts.drop("ID", axis=1)
    mask_my_accts = oppty['Affinity ID'].apply(lambda x: x in df_my_accts.index)

    oppty = oppty[mask_my_accts]

    df_designs = oppty[oppty["Opportunity Type"]=="Design"]
    df_designs = df_designs.set_index("Affinity ID")
    # df_designs = revenue_format(df_designs)                 #TODO: Necessary? could be accomplished in xlswriter
    df_designs = add_acct_alignments(df_designs, df_my_accts)
    df_designs = df_designs[out_cols]

    df_designs.to_excel(file_loc_store_designs, index=False)
    