'''
Antes de executar o processo, instale as dependências do projeto executando o seguinte comando no terminal:
pip install -r requirements.txt
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
import requests

class ExtrairDadosFaturas:

    # Inicializa variáveis de controle do processo.
    def __init__(self):
        self.var_driverNavegador = webdriver.Chrome()                           # Inicializa o Chrome
        self.var_dateDiaAtual = datetime.today()                                # Captura a data atual para comparar com a data de vencimento das faturas
        self.var_listFaturas = []                                               # Inicializa uma lista para armazenar informações das faturas
        self.var_strPastaFaturas = 'faturas/'                                   # Diretório onde as faturas serão salvas
        self.var_strUrlChallenge = 'https://rpachallengeocr.azurewebsites.net'  # URL Challenge
        os.makedirs(self.var_strPastaFaturas, exist_ok=True)                    # Cria o diretório para salvar as faturas, caso não exista

    def download_fatura(self, arg_strUrlFatura:str, arg_strNomeFatura:str):
        print("Realizando download da Fatura")

        # Faz uma requisição para obter o conteúdo da fatura
        var_responseFatura = requests.get(arg_strUrlFatura)
        
        # Salva o conteúdo da fatura
        with open(arg_strNomeFatura, 'wb') as arquivo:
            arquivo.write(var_responseFatura.content)

        print("Download da Fatura realizado..")

    def processar_pagina(self):
        print("Processando página")
        # Extrai o HTML da página
        var_bs4HtmlPagina = BeautifulSoup(self.var_driverNavegador.page_source, 'html.parser')

        # Procura pela tabela com ID tableSandbox no HTML
        var_bs4Tabela = var_bs4HtmlPagina.find('table', {'id': 'tableSandbox'})

        if var_bs4Tabela:
            # Captura as linhas da tabela
            var_bs4LinhasTabela = var_bs4Tabela.find('tbody').find_all('tr')

            # Percorre cada linha da tabela
            for linha in var_bs4LinhasTabela:
                # Captura todas as colunas da linha
                var_bs4ColunasTabela = linha.find_all('td')

                # Extrai os dados de cada coluna
                var_strNumeroFatura = var_bs4ColunasTabela[0].text.strip()
                var_strIdFatura = var_bs4ColunasTabela[1].text.strip()
                var_strDataVencimentoFatura = var_bs4ColunasTabela[2].text.strip()

                # Converte a data de vencimento de string para datetime
                var_dateDataVencimento = datetime.strptime(var_strDataVencimentoFatura, '%d-%m-%Y')

                # Extrai uma parte da URL para download da fatura
                var_strParteUrlFatura = var_bs4ColunasTabela[3].find('a')['href']

                # URL completa da fatura
                var_strUrlCompletaFatura = f'{self.var_strUrlChallenge}{var_strParteUrlFatura}'

                # Se a data de vencimento é anterior ou igual à data atual
                if var_dateDataVencimento <= self.var_dateDiaAtual:
                    # Caminho completo da fatura
                    var_strCaminhoFatura = f"{self.var_strPastaFaturas}{var_strIdFatura}_{var_strDataVencimentoFatura}.jpg"

                    # Faz o download da fatura
                    self.download_fatura(f'{var_strUrlCompletaFatura}', var_strCaminhoFatura)

                    # Adiciona os dados da fatura na lista
                    self.var_listFaturas.append({
                        "NumeroFatura": var_strNumeroFatura,
                        "DataVencimento": var_strDataVencimentoFatura,
                        "URLFatura": var_strUrlCompletaFatura
                    })

                    print("Dados salvos na lista")

    def navegar_paginas(self):
        
        print(f"Acessando site: {self.var_strUrlChallenge}")
        
        # Acessa o site
        self.var_driverNavegador.get(self.var_strUrlChallenge)
        self.var_driverNavegador.maximize_window()

        # Percorre as páginas da tabela
        while True:
            # Processa a página atual
            self.processar_pagina()

            # Tenta encontrar o botão "Next" para ir para a próxima página
            try:
                var_elementBotaoNext = self.var_driverNavegador.find_element(By.ID, 'tableSandbox_next')

                # Se o botão estiver desativado, significa que não tem mais páginas
                if 'disabled' in var_elementBotaoNext.get_attribute('class'):
                    print("Botão Next desativado, realizando break..")
                    break
                
                print("Acessando a proxima pagina da tabela")

                # Clica no botão para ir para a próxima página
                var_elementBotaoNext.click()
            except Exception as err:
                # Se ocorrer um erro ao tentar avançar, sai do loop
                print("Erro ao tentar avançar para a próxima página:", err)
                break

    def salvar_csv(self, arg_strCaminhoCsv:str='resultado_faturas.csv'):
        print("Criando arquivo CSV")

        # Cria um DataFrame com os dados da lista de faturas
        var_dfDadosExtraidos = pd.DataFrame(self.var_listFaturas)
        
        # Salva o DataFrame em um arquivo CSV
        var_dfDadosExtraidos.to_csv(arg_strCaminhoCsv, index=False)

        print("Arquivo CSV salvo")
    def fechar_navegador(self):
        print("Fechando Navegador")

        # Fecha o navegador
        self.var_driverNavegador.quit()

print("Inicializando Processo..")

# Inializa a classe Extrair Dados Faturas
var_clssScraper = ExtrairDadosFaturas()

# Interage com as páginas e extrai os dados das faturas
var_clssScraper.navegar_paginas()

# Salva os dados extraídos em um arquivo CSV e fecha o navegador.
var_clssScraper.salvar_csv()
var_clssScraper.fechar_navegador()

print("Extração dos dados concluído e CSV gerado.")
print("Processo finalizado")