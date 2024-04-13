import pandas as pd
from zipfile import ZipFile
import wget
import os, shutil

# ======================= #
# ======= CLASSES ======= #
# ======================= #
class Company:
    def __init__(self, company_code: int, bookkeping = None):
        self.company_code = company_code
        self.frequency = 'yearly'
        if bookkeping == None: self.bookkeping = 'ind'
        else: self.bookkeping = bookkeping
    
    # Method for pivoted yearly reports
    def DRE(self, begin:int, end:int):
        return yearly_stt(self.company_code, statement = f'DRE_{self.bookkeping}', begin = begin, end = end)
    def BP_Ativo(self, begin: int, end: int):
        return yearly_stt(self.company_code, statement = f'BPA_{self.bookkeping}', begin = begin, end = end)
    def BP_Passivo(self, begin:int, end:int):
        return yearly_stt(self.company_code, statement = f'BPP_{self.bookkeping}', begin = begin, end = end) 
    def DFC_MD(self, begin: int, end: int):
        return yearly_stt(self.company_code, statement = f'DFC_MD_{self.bookkeping}', begin = begin, end = end) 
    def DFC_MI(self, begin: int, end: int):
        return yearly_stt(self.company_code, statement = f'DFC_MI_{self.bookkeping}', begin = begin, end = end) 

class Historic(Company):
    def __init__(self, company_code: int, begin: int, end: int, bookkeping = None):
        super().__init__(company_code, bookkeping)
        self.begin = begin
        self.end = end

    ### Income Report Accounts
    def gross_revenue(self):
        return account_hist(self.company_code, f'DRE_{self.bookkeping}', account = '3.01', frequency = self.frequency, begin = self.begin, end = self.end)
    def net_revenue(self):
        return account_hist(self.company_code, f'DRE_{self.bookkeping}', account = '3.03', frequency = self.frequency, begin = self.begin, end = self.end)
    def ebitda(self):
        return account_hist(self.company_code, f'DRE_{self.bookkeping}', account = '3.05', frequency = self.frequency, begin = self.begin, end = self.end)
    def ebit(self):
        return account_hist(self.company_code, f'DRE_{self.bookkeping}', account = '3.07', frequency = self.frequency, begin = self.begin, end = self.end)
    def profit(self):
        return account_hist(self.company_code, f'DRE_{self.bookkeping}', account = '3.09', frequency = self.frequency, begin = self.begin, end = self.end)

# ====================== #
# ====== FUNTIONS ====== #
# ====================== #
def download(report: str, begin: int, end:int):
    '''
    This function is download both reports from dados.cvm.gov.br/data/CIA_ABERTA/DOC/

        report: 'dfp' for yearly reports
                'itr' for quarterly reports

        begin: initial year

        end: final year
    '''

    base_url = f'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/{report.upper()}/DADOS/'
    try:
        shutil.rmtree(f'statements/{report}')
        print(f"Deletada a pasta 'statements/{report}'")
    except:
        pass

    statements = ['BPA','BPP','DFC_MD','DFC_MI','DMPL','DRA','DRE','DVA']
    statements_type = ['ind', 'con']

    for year in range(begin, end + 1):

        wget.download(base_url + f'{report}_cia_aberta_{year}.zip')
        with ZipFile(f'{report}_cia_aberta_{year}.zip', 'r') as zip:
            print(' \nExtraindo arquivos...')
            zip.extractall(f'statements/{report}')
        os.remove(f'{report}_cia_aberta_{year}.zip')

    for stt in statements:
        for stt_tp in statements_type:
            os.mkdir(f'statements/{report}/{stt}_{stt_tp}')
            
            for year in range(begin, end +1):
                input_df = pd.read_csv(f'statements/{report}/{report}_cia_aberta_{stt}_{stt_tp}_{year}.csv',sep = ';', encoding= 'ISO-8859-1', decimal = ',')
                clean = input_df[input_df['ORDEM_EXERC'] == 'ÚLTIMO']
                
                clean.to_csv(f'statements/{report}/{stt}_{stt_tp}/{year}.csv', index = False)
                os.remove(f'statements/{report}/{report}_cia_aberta_{stt}_{stt_tp}_{year}.csv')
    return

def yearly_stt(company_code: int, statement: str, begin: int, end: int):
    '''
    This function returns the pivoted company statement from dfp report

        company_code: CVM code for the wanted company, can be find at b3 website

        statement:  'DRE_con' or 'DRE_ind' for income report
                    'BPA_con' or 'BPA_ind' for balance sheet (Assets)
                    'BPP_con' or 'BPP_con' for balance sheet (Liabilities)
                    'DCF_MD_con' or 'DFC_MD_ind' for cash flow (indirect method)
                    'DFC_MI_con' or 'DFC_MD_ind' for cash flow (direct method)
                    'DVA_con' or 'DVA_ind' for value added report
                    'DMPL_con' or 'DMPL ind' for statement of retained earnings

        begin: initial year

        end: final year
    '''
    main_path = f'statements/DFP/{statement}/'
    columns = ['DT_REFER', 'CD_CONTA', 'DS_CONTA', 'VL_CONTA']
    output_stt = pd.DataFrame(columns = columns)

    for year in range(begin, end +1):
        full_stt = pd.read_csv(f'{main_path}{year}.csv')

        company_statement = full_stt[full_stt['CD_CVM'] == company_code][columns]
        company_statement['DT_REFER'] = str(year)

        output_stt = pd.concat([output_stt, company_statement])
    return pd.pivot_table(output_stt, values = 'VL_CONTA',  columns = 'DT_REFER', index = ['CD_CONTA','DS_CONTA']).fillna(0)


def trim_stt(company_code: int, statement: str, begin: int, end: int):
    '''
    This function the pivoted DFP statement
    '''
    itr_main_path = f'statements/ITR/{statement}/'
    columns = ['DT_REFER', 'CD_CONTA', 'DS_CONTA', 'VL_CONTA']
    jointed = pd.DataFrame()

    for year in range(begin, end +1):
        itr_year = pd.read_csv(f'{itr_main_path}{year}.csv')
        cia_itr = itr_year[itr_year['CD_CVM'] == company_code]
        del itr_year

        cia_dfp = yearly_stt(company_code, statement, year, year)

        # Ajuste 4º trimestre
        three_trimesters_stt_aux = pd.pivot_table(cia_itr, values = 'VL_CONTA', columns='DT_REFER', index = ['CD_CONTA', 'DS_CONTA']).fillna(0)
        final_stt = three_trimesters_stt_aux
        three_trimesters_stt_aux['rows_sum'] = three_trimesters_stt_aux[f'{year}-03-31'] + three_trimesters_stt_aux[f'{year}-06-30'] + three_trimesters_stt_aux[f'{year}-09-30']
        final_stt[f'{year}-12-31'] = cia_dfp[f'{year}'] - three_trimesters_stt_aux['rows_sum']

        jointedcols = []
        for i in ['03','06','09', '12']:
            if i == '03' or i == '12': jointedcols.append(f'{year}-{i}-31')
            else: jointedcols.append(f'{year}-{i}-30')

        for col in jointedcols:
            jointed[col] = final_stt[col]
    return jointed.fillna(0)


def account_hist(company_code: int, statement: str, account: str, frequency: str, begin: int, end: int):
    '''
        Warning!!!
        Still doesn't work for quarterly reports
        
        company_code: CVM code for the wanted company, can be find at the B3 website

        statement:  'DRE_con' or 'DRE_ind' for income report
                    'BPA_con' or 'BPA_ind' for balance sheet (Assets)
                    'BPP_con' or 'BPP_con' for balance sheet (Liabilities)
                    'DCF_MD_con' or 'DFC_MD_ind' for cash flow (indirect method)
                    'DFC_MI_con' or 'DFC_MD_ind' for cash flow (direct method)
                    'DVA_con' or 'DVA_ind' for value added report
                    'DMPL_con' or 'DMPL ind' for statement of retained earnings report

        account: account number 

        frequency: 'yearly' para dados anuais
                   'quarterly' para dados trimestrias

        begin: initial year
        end: final year
    '''

    if frequency == 'yearly':
        company_statement = yearly_stt(
            company_code = company_code,
            statement = statement,
            begin = begin, end = end
            )
    elif frequency == 'quarterly':
        company_statement = trim_stt(
            company_code = company_code,
            statement = statement,
            begin = begin, end = end
            )

    return company_statement.loc[account]


# ÁREA DE TESTES

#download('ITR', 2020, 2023)

dre_2020_2023 = trim_stt(2437, 'DRE_con', 2020,2022)
print(dre_2020_2023)


#itr_year = pd.read_csv(f'statements/ITR/DRE_con/2020.csv')
#itr_cia = itr_year[itr_year['CD_CVM'] == 2437]
#del itr_year
#print(itr_cia)

#print(pd.pivot_table(itr_cia, values = 'VL_CONTA', columns='DT_REFER', index = ['CD_CONTA', 'DS_CONTA']).fillna(0))