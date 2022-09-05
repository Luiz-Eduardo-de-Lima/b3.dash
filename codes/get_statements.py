import pandas as pd
from zipfile import ZipFile
import wget
import os
from datetime import date
from codes.get_statements import *
from sqlite3 import *

def get_statements(begin, end, database):
    '''
    Retorna os balanços históricos das empresas de capital aberto disponíveis na CVM desde 2011.
    '''

    base_url = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/'
    try:
        os.system('rm -fr statements')
    except:
        pass
    
    for year in range(begin, end +1):
        wget.download(base_url + f'itr_cia_aberta_{year}.zip')
        with ZipFile(f'itr_cia_aberta_{year}.zip', 'r') as zip:
            print(' \nExtraindo arquivos...')
            zip.extractall('statements')
        os.system(f'rm -fr itr_cia_aberta_{year}.zip')
        
    statements = ['BPA','BPP','DFC_MD','DFC_MI','DMPL','DRA','DRE','DVA']
    statements_type = ['ind', 'con']

    for stt in statements:
        for stt_tp in statements_type:
            data = pd.DataFrame()
            for year in range(begin, end +1):
                data = pd.concat([
                    data,
                    pd.read_csv(f'statements/itr_cia_aberta_{stt}_{stt_tp}_{year}.csv', sep = ';', encoding= 'ISO-8859-1', decimal = ',')]
                    )
                os.system(f'rm -fr statements/itr_cia_aberta_{stt}_{stt_tp}_{year}.csv')
                
            data.to_sql(
                name = f'statements/{stt}_{stt_tp}_from_{begin}_to_{end}',
                con = database, index = False,
                if_exists='replace')
    
    data = pd.DataFrame()
    for year in range(begin, end +1):
        data = pd.concat([
            data,
            pd.read_csv(f'statements/itr_cia_aberta_{year}.csv', sep = ';', encoding= 'ISO-8859-1', decimal = ',')
            ])
        os.system(f'rm -fr statements/itr_cia_aberta_{year}.csv')

    data.to_sql(
        name = f'itr_cia_aberta_from_{begin}_to_{end}',
        con = database, index = False,
        if_exists='replace')      
    return