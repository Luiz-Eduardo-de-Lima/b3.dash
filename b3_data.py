import pandas as pd
from zipfile import ZipFile
import wget
import os

def get_statements(begin=int, end=int):

    '''
    Retorna os balanços históricos das empresas de capital aberto disponíveis na CVM desde 2011.
    '''

    base_url = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/'
    try:
        os.system('rm -fr statements')
    except:
        pass

    statements = ['BPA','BPP','DFC_MD','DFC_MI','DMPL','DRA','DRE','DVA']
    statements_type = ['ind', 'con']

    for year in range(begin, end +1):
        wget.download(base_url + f'itr_cia_aberta_{year}.zip')
        with ZipFile(f'itr_cia_aberta_{year}.zip', 'r') as zip:
            print(' \nExtraindo arquivos...')
            zip.extractall('statements')
        os.system(f'rm -fr itr_cia_aberta_{year}.zip')

    for stt in statements:
        for stt_tp in statements_type:
            os.system(f'mkdir statements/{stt}_{stt_tp}')
            
            for year in range(begin, end +1):
                input_df = pd.read_csv(
                            f'statements/itr_cia_aberta_{stt}_{stt_tp}_{year}.csv',
                            sep = ';', encoding= 'ISO-8859-1', decimal = ','
                )
                
                clean = input_df[input_df['ORDEM_EXERC'] == 'ÚLTIMO']
                
                clean.to_csv(f'statements/{stt}_{stt_tp}/{year}.csv', index = False)
                os.system(f'rm -fr statements/itr_cia_aberta_{stt}_{stt_tp}_{year}.csv')
    return

def select_stt(company_code = int, statement = str, begin = int, end = int):
    out_csv = pd.DataFrame()
    
    for year in range(begin, end + 1):
        path =  f'statements/{statement}/{year}.csv'
        
        stt = pd.read_csv(path)
        stt = stt['CD_CVM' == company_code]

        out_csv = pd.concat([out_csv, stt])
        
    return out_csv