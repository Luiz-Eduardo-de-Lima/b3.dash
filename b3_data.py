import pandas as pd
from zipfile import ZipFile
import wget
import os

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

def pivoted_statement(company_code: int, statement: str, begin: int, end: int):
    '''
    This function the pivoted DFP statement
    '''
    main_path = f'statements/dfp/{statement}/'
    columns = ['DT_REFER', 'CD_CONTA', 'DS_CONTA', 'VL_CONTA']
    output_stt = pd.DataFrame(columns = columns)

    for year in range(begin, end +1):
        full_stt = pd.read_csv(f'{main_path}{year}.csv')

        company_statement = full_stt[full_stt['CD_CVM'] == company_code][columns]
        company_statement['DT_REFER'] = str(year)

        output_stt = pd.concat([output_stt, company_statement])
    return pd.pivot_table(year, values = 'VL_CONTA',  columns = 'DT_REFER', index = 'CD_CONTA')

pivoted_statement(1023, 'DRE_con', 2020, 2021)