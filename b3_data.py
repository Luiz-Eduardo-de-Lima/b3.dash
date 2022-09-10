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
                
                clean = input_df[['DENOM_CIA', 'CD_CVM', '']]
                
                input_df.to_csv(f'statements/{stt}_{stt_tp}/{year}.csv', index = False)
                os.system(f'rm -fr statements/itr_cia_aberta_{stt}_{stt_tp}_{year}.csv')
    return

#def stt_to_excel(company_code: str, statement: str):
#    '''
#        Entre o código da CVM da empresa que deseja e o 
#        demonstrativo desejado:
#    '''

#    base_dir = f'statements/{statement}'
#    stt_years = os.listdir(base_dir)

    #for stt_y in stt_years:
        #pd.read_csv(
            #base_dir + stt_y, encoding = 'UTF_8'
        #)['']
