import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import re

def rename_cols(df):
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]

def gen_fyear(df, date_col):
    df['year'] = df[date_col].dt.year
    df['month'] = df[date_col].dt.month
    df['fyear'] = np.nan
    for y in range(int(df.year.min()), int(df.year.max()) + 2):
        print(y)
        df.loc[((df.year == y) & (df.month.isin(range(1, 7)))) 
               | ((df.year == y-1) & (df.month.isin(range(7, 13)))), 'fyear'] = y
#     df['fyear'] = df.fyear.astype('int')

def check_id_unique(df, id):
    if df[id].drop_duplicates().shape[0] == df.shape[0]:
        return True
    else:
        return False

def des_df(df):
    print(df.shape)
    print(df.dtypes)
    print(fillRates(df))
    print(df.head())
#     print(tabulate(df, headers='keys', tablefmt='psql'))

def print_missing_pattern(df, colsum):
    missing_pattern = pd.concat([df[colsum].value_counts().divide(df.shape[0]).sort_index(), 
                                 df.groupby(colsum).mean().reset_index(drop=True), 
                                 df.groupby(colsum).sum().reset_index(drop=True)], axis=1).reset_index()
    missing_pattern.columns = [colsum, 'percentage', 'inpsn_pct', 'wbnr_pct', 'inpsn_count', 'wbnr_count']
    f_cols = ['percentage', 'inpsn_pct', 'wbnr_pct']
    for col in f_cols:
        missing_pattern[col] = (missing_pattern[col]*100).map('{:,.1f}%'.format)
    print(missing_pattern)

def dichotomize(df):
    try:
        df = df.to_frame()
    except:
        pass
    
    for col in df.columns:
        df.loc[df[col] > 1, col] = 1
    return df

def fillRates(df, pct=0.9):
    """
    pct: Fillrate threshhold below which a column will be listed. 
    """
    fillrates = df.count() / df.shape[0]
    print(fillrates[fillrates < pct].sort_values())
    return fillrates

def get_cols(df):
    import re
    p = re.compile('(id|key|number)$', re.IGNORECASE)
    non_id_cols = [c for c in df.columns if not p.search(c)]
    return non_id_cols

def describe_continuous(df):
    cols = df.select_dtypes(include=['float64', 'int64']).columns.values
    import re
    p = re.compile('(id|key|number)$', re.IGNORECASE)
    cols = [c for c in cols if not p.search(c)]
    print(df[cols].describe())
    plt.style.use('bmh')
    for c in cols:
        print(c)
        srs = df[c].dropna()
        val_count = len(df[c].drop_duplicates())
        if val_count > 50:
            val_count = val_count // 2 + 1
        elif val_count > 100:
            val_count = val_count // 4 + 1
            if val_count > 50:
                val_count = 50
        plt.hist(srs, histtype="stepfilled", bins=val_count, alpha=0.8)
        plt.show()
    
def describe_categorical(df):
    cols = df.select_dtypes(include=['object']).columns.values
    import re
    p = re.compile('(id|key|number)$', re.IGNORECASE)
    cols = [c for c in cols if not p.search(c)]
    for c in cols:
        print('\n', c)
        print(df[c].value_counts())
        
def describe_table(name):
    """
    name: string representing the name of the table. 
    """
    df = psql.read_sql('select top 100000 * from dbo.' + name , cnxn)
    df.head()
    fillRates(df)
    describe_continuous(df)
    describe_categorical(df)