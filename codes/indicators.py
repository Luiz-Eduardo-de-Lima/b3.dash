import pandas as pd

def hist_ebit(company = str):
    dre = pd.read_csv('statements/DRE_con_from_2011_2012.csv', decimal = ',', sep = ';')['DENOM_CIA' == company]
    

    return