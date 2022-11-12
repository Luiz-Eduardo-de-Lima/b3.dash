import pandas as pd
from zipfile import ZipFile
import wget
import os

def dfp_download(begin: int, end: int):

    '''
    Baixa as DFP's (Demonstrações Financeiras Padronizadas) do site da CVM.
    Relatórios disponíveis a partir de 2011.
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
                input_df = pd.read_csv(f'statements/dfp/dfp_cia_aberta_{stt}_{stt_tp}_{year}.csv',sep = ';', encoding= 'ISO-8859-1', decimal = ',')
                clean = input_df[input_df['ORDEM_EXERC'] == 'ÚLTIMO']
                
                clean.to_csv(f'statements/dfp/{stt}_{stt_tp}/{year}.csv', index = False)
                os.system(f'rm -fr statements/dfp/dfp_cia_aberta_{stt}_{stt_tp}_{year}.csv')
    return

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
        wget.download(base_url + f'ditr_cia_aberta_{year}.zip')
        with ZipFile(f'itr_cia_aberta_{year}.zip', 'r') as zip:
            print(' \nExtraindo arquivos...')
            zip.extractall('statements/itr')
        os.system(f'rm -fr dfp_cia_aberta_{year}.zip')

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

def dfp_pivoted(company_code: int, statement: str, begin: int, end: int):
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
    return pd.pivot_table(output_stt, values = 'VL_CONTA',  columns = 'DT_REFER', index = ['CD_CONTA','DS_CONTA'])

def itr_pivoted(company_code: int, statement: str, begin: int, end: int):
    columns: list = ['DT_REFER', 'CD_CONTA', 'DS_CONTA', 'VL_CONTA']
    jointed_stt = pd.DataFrame(columns = columns)
    itr_by_year = []
    for year in range(begin,end +1):
        itr = pd.read_csv(f'statements/itr/{statement}/{year}.csv')
        comp_itr = itr[itr['CD_CVM'] == company_code][columns]
        del itr

        dfp = pd.read_csv(f'statements/dfp/{statement}/{year}.csv')[columns]
        comp_dfp = dfp[dfp['CD_CVM'] == company_code][columns]
        del dfp
        
        comp_dfp['VL_CONTA'] = dfp['VL_CONTA'] - comp_itr.groupby('CD_CONTA', axis = 1).sum()['VL_CONTA']

        itr_by_year.append(pd.concat([itr,dfp]))

    jointed_stt = pd.concat(itr_by_year)
    return pd.pivot_table(jointed_stt, values = 'VL_CONTA',  columns = 'DT_REFER', index = ['CD_CONTA','DS_CONTA'])

