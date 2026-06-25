import matplotlib.pyplot as plt
import plotly.express as px

def _aplicar_tema_escuro(ax):
    """Função privada para estilização premium do Matplotlib"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#555555')
    ax.spines['bottom'].set_color('#555555')
    ax.tick_params(colors='white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.grid(axis='x', linestyle='--', alpha=0.3)

def plotar_mapa_mundi(df_filtrado):
    """Gera um GLOBO 3D interativo de medalhas"""
    df_eventos = df_filtrado.drop_duplicates(subset=['id_edicao', 'evento', 'noc_pais', 'medalha'])
    df_mapa = df_eventos.groupby(['pais', 'ISO3'])['medalha'].count().reset_index()
    
    # Criando o Globo
    fig = px.choropleth(
        df_mapa, locations="ISO3", color="medalha", hover_name="pais",
        color_continuous_scale="Plasma", # Cores neon/vibrantes
        title="Globo de Domínio (Gire com o mouse)"
    )
    
    # Configuração 3D e Tema Escuro
    fig.update_layout(
        template="plotly_dark",
        geo=dict(
            showframe=False, 
            showcoastlines=True, coastlinecolor="rgba(255, 255, 255, 0.1)",
            projection_type='orthographic', # ISSO AQUI FAZ VIRAR UM GLOBO 3D
            showland=True, landcolor="#1e1e1e",
            showocean=True, oceancolor="#0e1117",
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)', 
        margin=dict(l=0, r=0, t=40, b=0)
    )
    return fig

def plotar_ranking_top10(df_filtrado):
    df_eventos = df_filtrado.drop_duplicates(subset=['id_edicao', 'evento', 'noc_pais', 'medalha'])
    ranking = df_eventos['pais'].value_counts().nlargest(10).sort_values()
    
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0E1117')
    ax.set_facecolor('#0E1117')
    
    ax.barh(ranking.index, ranking.values, color='#00C59E')
    ax.set_title('Top 10 Países Medalhistas', pad=15)
    ax.set_xlabel('Quantidade de Eventos Ganhos')
    _aplicar_tema_escuro(ax)
    
    plt.tight_layout()
    return fig

def plotar_biotipo_atletas(df_pais):
    df_fisico = df_pais.dropna(subset=['altura', 'peso'])
    
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0E1117')
    ax.set_facecolor('#0E1117')
    
    ax.scatter(df_fisico['peso'], df_fisico['altura'], alpha=0.7, c='#FFD700', edgecolors='white')
    ax.set_title('Biotipo dos Medalhistas (Peso x Altura)', pad=15)
    ax.set_xlabel('Peso (kg)')
    ax.set_ylabel('Altura (cm)')
    _aplicar_tema_escuro(ax)
    
    plt.tight_layout()
    return fig