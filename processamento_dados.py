import pandas as pd
import numpy as np

# função de leitura dos arquivos, pegando por padrao na pasta dados
def carregar_csvs(pasta="dados/"):
    dfs = {
        'atletas': pd.read_csv(pasta + "Olympic_Athlete_Event_Details.csv"),
        'biografia': pd.read_csv(pasta + "Olympic_Athlete_Biography.csv"),
        'paises': pd.read_csv(pasta + "Olympic_Country_Profiles.csv"),
        'idh': pd.read_csv(pasta + "Human Development Index - Full.csv"),
        'populacao': pd.read_csv(pasta + "countries of the world.csv"),
        'clima': pd.read_csv(pasta + "GlobalLandTemperaturesByCountry.csv"),
        'jogos': pd.read_csv(pasta + "Olympic_Games_Summary.csv")
    }
    return dfs

#funcao de limpeza
def limpar_dados_socioeconomicos(df_idh, df_populacao, df_clima):
    # limpando o idh 
    idh_limpo = df_idh[['ISO3', 'Country', 'Human Development Index (2021)']].dropna()
    idh_limpo = idh_limpo.rename(columns={'Human Development Index (2021)': 'IDH'})
    
    #  limpando população
    populacao_limpa = df_populacao[['Country', 'Population']].dropna()
    
    # pegando media e ajustando dados do clima
    clima_limpo = df_clima.groupby('Country')['AverageTemperature'].mean().reset_index()
    clima_limpo = clima_limpo.rename(columns={'AverageTemperature': 'Clima_Medio'})
    
    return idh_limpo, populacao_limpa, clima_limpo

#limpando e mesclando os dados dos atletas/jogos
def limpar_dados_atletas(df_atletas, df_biografia, df_jogos):

    biografia_limpa = df_biografia.drop(columns=['country_noc', 'country'], errors='ignore')
    
    # mesclando atleta e biografia
    df_mesclado = pd.merge(df_atletas, biografia_limpa, on='athlete_id', how='inner')
    
    # adicionando o ano da edição
    jogos_limpo = df_jogos[['edition_id', 'year']]
    df_mesclado = pd.merge(df_mesclado, jogos_limpo, on='edition_id', how='left')
    
    return df_mesclado

# rodando e dando ajustes finais
def obter_dataset_consolidado():
    dfs = carregar_csvs()
    
    # limpezas isoladas
    idh, populacao, clima = limpar_dados_socioeconomicos(dfs['idh'], dfs['populacao'], dfs['clima'])
    atletas_base = limpar_dados_atletas(dfs['atletas'], dfs['biografia'], dfs['jogos'])
    
    # construindo tabela final
    df_principal = pd.merge(atletas_base, dfs['paises'], left_on='country_noc', right_on='noc', how='left')
    df_principal = pd.merge(df_principal, idh, left_on='country', right_on='Country', how='left')
    df_principal = pd.merge(df_principal, populacao, left_on='country', right_on='Country', how='left')
    df_principal = pd.merge(df_principal, clima, left_on='country', right_on='Country', how='left')
    
    # manter medalhistas e converter tipos
    df_principal = df_principal.dropna(subset=['medal'])
    df_principal['year'] = df_principal['year'].fillna(0).astype(int)
    
    # traduzindo os dados pra pt
    df_principal = df_principal.rename(columns={
        'year': 'ano',
        'sport': 'esporte',
        'country': 'pais',
        'edition_id': 'id_edicao',
        'event': 'evento',
        'medal': 'medalha',
        'height': 'altura',
        'weight': 'peso',
        'athlete': 'atleta',
        'country_noc': 'noc_pais',
        'Population': 'populacao',
        'Clima_Medio': 'clima_medio'
    })
    
    return df_principal