import pandas as pd
import numpy as np
import streamlit as st

# ==========================================
# 1. FUNÇÕES (A máquina precisa ser construída primeiro)
# ==========================================

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
    
    ano_nascimento = pd.to_datetime(df['date_of_birth'], errors='coerce').dt.year #padronizando a data de nascimento em ano
    df['idade_atleta'] = 2024 - ano_nascimento
    df = df.drop(columns=['date_of_birth']) #deletando as colunas que não vão ser ultilizadas
    return df

def limpeza_clima(df):
    df['Ano'] = pd.to_datetime(df['dt'], errors='coerce').dt.year #convertendo a data em ano 
    df = df[(df['Ano'] >= 2000) & (df['Ano'] <= 2013)] #separando somente os dados relevantes e excluindo o resto
    df = df.drop(columns=['dt'])
    df = df.groupby('Country')['AverageTemperature'].mean().reset_index()
    return df


# ==========================================
# 2. RODANDO A MÁQUINA (Agora que as funções existem, usamos elas)
# ==========================================

st.title("Painel de Teste de Dados 🚀")

# Dados do Clima
df_clima_bruto = carregar_dados("GlobalLandTemperaturesByCountry.csv")
df_clima_limpo = limpeza_clima(df_clima_bruto)

# Dados dos Atletas
df_atletas_bruto = carregar_dados("2024_medalists_all.csv") 
df_atletas_limpo = limpeza_atletas(df_atletas_bruto)


# ==========================================
# 3. MOSTRANDO NA TELA
# ==========================================

st.subheader("🌍 Dados de Clima (Tratados)")
st.dataframe(df_clima_limpo.head(10))

st.subheader("🏃 Dados dos Atletas (Tratados)")
st.dataframe(df_atletas_limpo.head(10))


# ==========================================
# 4. O MODO DETETIVE (ÚLTIMA COISA DO ARQUIVO!)
# ==========================================

st.subheader("🔍 Modo Detetive: Países que não bateram")

paises_atletas = set(df_atletas_limpo['country_medal'].dropna().unique())
paises_clima = set(df_clima_limpo['Country'].dropna().unique())

paises_problematicos = paises_atletas - paises_clima

# Mostra na tela os países da tabela de atletas que precisam ter o nome traduzido!
st.write(paises_problematicos)