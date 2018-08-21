# -*- coding: latin-1 -*-

import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
import bs4
from selenium import webdriver
import time


def baixar_tabela():
        
    url = "http://www.nware.com.br/tbca/tbca/"

    browser = webdriver.Chrome("chromedriver.exe") #replace with .Firefox(), or with the browser of your choice
    browser.get(url) #navigate to the page

    produtos = pd.read_csv("lista_alimentos.csv", encoding='latin1', sep=";")

    tabelas = []

    for cod in produtos["Cod"]:
        produto = str(produtos[produtos["Cod"] == cod]["Produto"])
        print('{} - {}'.format(cod, produto))
        browser.execute_script("getProdMedida('{0}')".format(cod))
        time.sleep(1)
        innerHtml = browser.execute_script("return document.body.innerHTML")
        soup = bs4.BeautifulSoup(innerHtml)
        table = pd.read_html(str(soup.find(id="itproduto")), encoding='latin1')[0]
        table = table.iloc[:,:3]
        table["Cod"] = cod
        table["Produto"] = produto
        tabelas.append(table)

    df = pd.concat(tabelas)
    pd.to_pickle(df,"tbca.pickle")

#baixar_tabela()

df = pd.read_pickle("tbca.pickle")
df[(df['Componente'] == 'Energia') & (df['Unidades'] == 'kcal')]['Valor por 100 g']
