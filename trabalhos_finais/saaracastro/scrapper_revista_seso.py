# -*- coding: utf-8 -*-
"""scrapper_revista_seso.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Y9lMG8dtS4d2vFt9D6z5vHUtsbS9Glfh

**Importações**
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import json

def abrir_url(url):
  url_aberta = urlopen(url)
  bs = BeautifulSoup(url_aberta.read(), 'lxml')
  return bs

def obter_edicoes(bs):
  bloco_edicoes = bs.select_one("ul[class='issues_archive']")
  lista_edicoes = bloco_edicoes.find_all('li')

  edicoes_tratadas = []

  for edicao in lista_edicoes:
    nome = edicao.find("a").text
    link = edicao.find("a")['href']
    serie = edicao.find("div",{'class':'series'}).text
    
    edicoes_tratadas.append({
        "nome": nome.strip(),
        "url": link,
        "serie": serie.strip(),
     })
    
  return edicoes_tratadas

def obter_detalhes_edicao(bs, edicao_crua):
  edicao_enriquecida = edicao_crua
  data_publicacao = None
  publicacoes = []

  # Adiciona informacao "data de publicação" à edição
  data_publicacao = bs.find("span", {'class': 'value'}).text
  edicao_enriquecida['data_de_publicacao'] = data_publicacao.strip()

  # Adiciona informacao "publicacoes" à edição
  espaco_tematico = bs.find("ul", {'class': ['cmp_article_list', 'articles']})
  lista_publicacoes = espaco_tematico.find_all('li')

  for item in lista_publicacoes:
    titulo = item.find("a").text
    link = item.find("a")['href']
    
    publicacoes.append({
        "titulo": titulo.strip(),
        "url": link,
    })
  
  edicao_enriquecida['publicacoes'] = publicacoes

  return edicao_enriquecida

def obter_detalhes_publicacao(bs_edicao, publicacao):
  titulo = bs_edicao.find('h1',{'class':'page_title'}).text
  print(titulo)
  bloco_conteudos = bs_edicao.select_one("div[class='main_entry']")

  # autor = bloco_conteudos.find('spam',{'class':'name'}).text
  # palavra_chave = bloco_conteudos.find('section',{})

  return publicacao

"""Chamando as funções"""

url_raiz = 'https://periodicos.ufsc.br/index.php/katalysis/issue/archive'


bs_raiz = abrir_url(url_raiz)
edicoes= obter_edicoes(bs_raiz)

# Agora vamos acessar cada edicao individualmente e obter mais informacoes,
# tal como, as publicações
for edicao in edicoes:
  url_edicao = edicao.get('url')
  bs_edicao = abrir_url(url_edicao)
  edicao = obter_detalhes_edicao(bs_edicao, edicao)

  

json_object = json.dumps(edicoes, indent = 4) 
print(json_object)

# teste (em andamento)
publicacao = {}
bs_publicacao = abrir_url('https://periodicos.ufsc.br/index.php/katalysis/article/view/84365')
publicacao= obter_detalhes_publicacao(bs_publicacao, publicacao)
print(publicacao)
