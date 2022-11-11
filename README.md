# B3_data

Hoje o mercado financeiro ainda é muito dependente dos sistemas clássicos de planilhas. Porém, com a popularização das linguagens de programação o setor exige novas ferramentas para possibilitar essas análise. O B3_data é um projeto criado para possibilitar a análise fundamentalista utilizando a linguagem Python de forma simples.

Futuramente esse projeto servirá de base para uma aplicação mais robusta com interface gráfica, ferramentas de análise, projeções e análise quantitativa.

Fonte dos dados: https://dados.cvm.gov.br/

## To do:

- [x] Download das DFP'S (Demonstrações Financeiras Padronizadas)
- [X] Download das ITR'S (Relatório de Informações Trimestrais)
- [X] Exportação dos demonstrativos pivotados em .xlsx
- [ ] Cálculo de indicadores fundamentalistas (P/L, Margem Líquida, ROE, ROIC, etc)
- [ ] Métrica para fluxo de caixa descontado (K<sub>e</sub>, K<sub>d</sub>, Wacc, etc)
- [ ] Fluxo de caixa descontado
- [ ] Notebook de exemplo

## Uma breve explicação dos relatórios contábeis:

### Publicações

As CIA's precisam publicar seus demonstrativos 4 vezes no ano, 3 dessas vezes são demonstrativos trimestrais, i.e., os balanços apresentam informações referentes apenas ao exercício do trimestre, essas publicações são encontrados nas ITR's. Porém é estranho, não? O ano tem 4 trimestres e apenas 3 são publicados.

O que ocorre é que não há uma publicação referente apenas ao exercício do 4º trimestre. O último relatório a ser publicado é referente ao exercício anual. Obviamente o ajuste é simples, a soma do resultado dos trimestres do ano referência subtraídos dos resultado anual

