import pandas as pd
from zipfile import ZipFile
import wget
import os

def get_statements(begin: int, end: int):
    itr_download(begin, end)
    dfp_download(begin, end)

def itr_download(begin: int, end: int):

    '''
    Retorna os balanços históricos das empresas de capital aberto disponíveis na CVM desde 2011.
    '''

    base_url = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/'
    try: os.system('rm -fr statements/itr')
    except: pass

    statements = ['BPA','BPP','DFC_MD','DFC_MI','DMPL','DRA','DRE','DVA']
    statements_type = ['ind', 'con']

    for year in range(begin, end +1):
        wget.download(base_url + f'itr_cia_aberta_{year}.zip')
        with ZipFile(f'itr_cia_aberta_{year}.zip', 'r') as zip:
            print(' \nExtraindo arquivos...')
            zip.extractall('statements/itr')
        os.system(f'rm -fr itr_cia_aberta_{year}.zip')

    for stt in statements:
        for stt_tp in statements_type:
            os.system(f'mkdir statements/itr/{stt}_{stt_tp}')
            
            for year in range(begin, end +1):
                input_df = pd.read_csv(
                    f'statements/itr/itr_cia_aberta_{stt}_{stt_tp}_{year}.csv',
                    sep = ';', encoding= 'ISO-8859-1', decimal = ','
                )
                
                clean = input_df[input_df['ORDEM_EXERC'] == 'ÚLTIMO']
                
                clean.to_csv(f'statements/itr/{stt}_{stt_tp}/{year}.csv', index = False)
                os.system(f'rm -fr statements/itr/itr_cia_aberta_{stt}_{stt_tp}_{year}.csv')
    return

def dfp_download(begin: int, end: int):

    '''
    Retorna os balanços históricos das empresas de capital aberto disponíveis na CVM desde 2011.
    '''

    base_url = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/'
    try: os.system('rm -fr statements/dfp')
    except: pass

    statements = ['BPA','BPP','DFC_MD','DFC_MI','DMPL','DRA','DRE','DVA']
    statements_type = ['ind', 'con']

    for year in range(begin, end +1):
        wget.download(base_url + f'dfp_cia_aberta_{year}.zip')
        with ZipFile(f'dfp_cia_aberta_{year}.zip', 'r') as zip:
            print(' \nExtraindo arquivos...')
            zip.extractall('statements/dfp')
        os.system(f'rm -fr dfp_cia_aberta_{year}.zip')

    for stt in statements:
        for stt_tp in statements_type:
            os.system(f'mkdir statements/dfp/{stt}_{stt_tp}')
            
            for year in range(begin, end +1):
                input_df = pd.read_csv(
                            f'statements/dfp/dfp_cia_aberta_{stt}_{stt_tp}_{year}.csv',
                            sep = ';', encoding= 'ISO-8859-1', decimal = ','
                )
                
                clean = input_df[input_df['ORDEM_EXERC'] == 'ÚLTIMO']
                
                clean.to_csv(f'statements/dfp/{stt}_{stt_tp}/{year}.csv', index = False)
                os.system(f'rm -fr statements/dfp/dfp_cia_aberta_{stt}_{stt_tp}_{year}.csv')

def show_statement(company_code: int, statement: str, begin: int, end: int):
    '''
    This function return the statement of a selected company.

    In the ITR document there is no information about the forth trimestrer of the year.
    This happens because in the 4th trimestre companies need to publish the statements refering to the entire year activity.
    In order to see this information we need to subtract the sum of the previous three trimesters from the DFP document.
    '''
    columns = ['DT_REFER', 'CD_CONTA', 'DS_CONTA', 'VL_CONTA']
    year_stt = pd.DataFrame()

    for year in range(begin, end + 1):
        # ========================== #
        # == 1st to 3rd trimester == #
        # ========================== #
        trimestral_statements_path = f'statements/itr/{statement}/{year}.csv'
        itr_statement = pd.read_csv(trimestral_statements_path)
        itr_statement = itr_statement[itr_statement['CD_CVM'] == company_code][columns]

        trimestral_sum = itr_statement[['CD_CONTA', 'DS_CONTA', 'VL_CONTA']].groupby(['CD_CONTA', 'DS_CONTA']).sum() + (- 1)
        # =================== #
        # == 4th trimester == #
        # =================== #
        
        forth_trimester_path = f'statements/dfp/{statement}/{year}.csv'
        forth_trimester = pd.read_csv(forth_trimester_path)[columns]

        adjusted_forth_trimester = pd.concat([forth_trimester, trimestral_sum])
        del forth_trimester

        year_stt = pd.concat([itr_statement, adjusted_forth_trimester], ignore_index=True)
        pivoted_year_stt = pd.pivot_table(year_stt, values = 'VL_CONTA', columns=['DT_REFER'], index = ['CD_CONTA', 'DS_CONTA'])
        
        year_stt = pivoted_year_stt.merge(year_stt, how = 'outer', on = ['CD_CONTA', 'DS_CONTA'])

    return year_stt

def select_stt(company_code: int, statement: str, begin: int, end: int):
    out_csv = pd.DataFrame()
    
    for year in range(begin, end + 1):
        path =  f'statements/{statement}/{year}.csv'
        
        stt = pd.read_csv(path)
        stt = stt[stt['CD_CVM'] == company_code]

        out_csv = pd.concat([out_csv, stt])
        
    return out_csv