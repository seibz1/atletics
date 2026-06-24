import pandas as pd
import numpy as np

# --- 1. FUNÇÕES DE LEITURA (Acesso a Dados) ---
def carregar_csvs(pasta="dados/"):
    """Responsável apenas por ler os arquivos do disco."""
    dfs = {
        'athletes': pd.read_csv(pasta + "Olympic_Athlete_Event_Details.csv"),
        'bio': pd.read_csv(pasta + "Olympic_Athlete_Biography.csv"),
        'countries': pd.read_csv(pasta + "Olympic_Country_Profiles.csv"),
        'hdi': pd.read_csv(pasta + "Human Development Index - Full.csv"),
        'pop': pd.read_csv(pasta + "countries of the world.csv"),
        'clima': pd.read_csv(pasta + "GlobalLandTemperaturesByCountry.csv"),
        'games': pd.read_csv(pasta + "Olympic_Games_Summary.csv")
    }
    return dfs

# --- 2. FUNÇÕES DE LIMPEZA E ENGENHARIA DE DADOS (Business Logic) ---
def limpar_dados_socioeconomicos(df_hdi, df_pop, df_clima):
    """Filtra, limpa nulos e padroniza as bases socioeconômicas."""
    # IDH: Pegar apenas 2021 e remover nulos
    hdi_clean = df_hdi[['ISO3', 'Country', 'Human Development Index (2021)']].dropna()
    hdi_clean = hdi_clean.rename(columns={'Human Development Index (2021)': 'IDH'})
    
    # População
    pop_clean = df_pop[['Country', 'Population']].dropna()
    
    # Clima: Agrupar média histórica por país
    clima_clean = df_clima.groupby('Country')['AverageTemperature'].mean().reset_index()
    clima_clean = clima_clean.rename(columns={'AverageTemperature': 'Clima_Medio'})
    
    return hdi_clean, pop_clean, clima_clean

def limpar_dados_atletas(df_athletes, df_bio, df_games):
    """Remove colunas redundantes e cruza dados vitais dos atletas com as edições."""
    # Remover colunas que causam conflito
    bio_clean = df_bio.drop(columns=['country_noc', 'country'], errors='ignore')
    
    # Merge Atleta + Biografia
    df_merged = pd.merge(df_athletes, bio_clean, on='athlete_id', how='inner')
    
    # Adicionar o Ano da Edição
    games_clean = df_games[['edition_id', 'year']]
    df_merged = pd.merge(df_merged, games_clean, on='edition_id', how='left')
    
    return df_merged

# --- 3. ORQUESTRADOR PRINCIPAL ---
def obter_dataset_consolidado():
    """Função principal que orquestra a pipeline de dados."""
    dfs = carregar_csvs()
    
    # Limpezas isoladas
    hdi, pop, clima = limpar_dados_socioeconomicos(dfs['hdi'], dfs['pop'], dfs['clima'])
    atletas_base = limpar_dados_atletas(dfs['athletes'], dfs['bio'], dfs['games'])
    
    # Consolidação Final
    df_master = pd.merge(atletas_base, dfs['countries'], left_on='country_noc', right_on='noc', how='left')
    df_master = pd.merge(df_master, hdi, left_on='country', right_on='Country', how='left')
    df_master = pd.merge(df_master, pop, left_on='country', right_on='Country', how='left')
    df_master = pd.merge(df_master, clima, left_on='country', right_on='Country', how='left')
    
    # Engenharia de Features: Manter apenas medalhistas e converter tipos
    df_master = df_master.dropna(subset=['medal'])
    df_master['year'] = df_master['year'].fillna(0).astype(int)
    
    return df_master