import pandas as pd
import numpy as np

# função generica que carrega os dados
def carregar_dados(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo)
    return df   #pandas lê o arquivo e retorna na variavel

# função generica que limpa as linhas nulas
def limpeza(df):
  df_limpo = df.dropna(how='all')
  return df_limpo #pandas remove linhas onde todas as colunas estao vazias

# função especifica que limpa os dados dos atletas
def limpeza_atletas(df):
   
    colunas_interesse = [
        'medalist_name', 'medal', 'date_of_birth', 'sex_or_gender', 
        'country_medal', 'place_of_birth', 'sport', 'event_part_of', 
        'lat', 'lon', 'nuts2_population', 'nuts2_gdp'
    ]
    df = df[colunas_interesse] # selecionando as colunas que vão ser usadas e descartando o resto
    
    df = df.drop_duplicates() #remove a linha apenas se for exatamente igual a outra
    
    df['nuts2_population'] = pd.to_numeric(df['nuts2_population'], errors='coerce')
    df['nuts2_gdp'] = pd.to_numeric(df['nuts2_gdp'], errors='coerce') #padronizando os dados idh e populacao
    
    ano_nascimento = pd.to_datetime(df['date_of_birth'], errors='coerce').dt.year #padronizandoa a data de nascimento em ano
    df['idade_atleta'] = 2024 - ano_nascimento
    df = df.drop(columns=['date_of_birth']) #deletando as colunas que não vão ser ultilizadas
    return df


def limpeza_clima(df):
    df['Ano'] = pd.to_datetime(df['dt'], errors='coerce').dt.year #convertendo a data em ano 
    df = df[(df['Ano'] >= 2000) & (df['Ano'] <= 2013)] #separando somente os dados relevantes e excluindo o resto
    df = df.drop(columns=['dt'])

    df = df.groupby('Country')['AverageTemperature'].mean().reset_index()
    return df