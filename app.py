import streamlit as st
import pandas as pd
import processamento_dados as pdados
import graficos as graf

st.set_page_config(page_title="Dashboard Olímpico Avançado", layout="wide")

@st.cache_data
def load_data():
    return pdados.obter_dataset_consolidado()

try:
    df_master = load_data()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# --- BARRA LATERAL (FILTRO DE TEMPO) ---
st.sidebar.title("Máquina do Tempo ⏳")
st.sidebar.markdown("Este filtro afeta o projeto inteiro.")
anos_disponiveis = ["Todas as Edições"] + sorted(df_master[df_master['year'] > 0]['year'].unique().tolist(), reverse=True)
ano_selecionado = st.sidebar.selectbox("Selecione a Edição (Ano):", anos_disponiveis)

if ano_selecionado != "Todas as Edições":
    df_ano = df_master[df_master['year'] == ano_selecionado]
else:
    df_ano = df_master

st.title("Análise Olímpica Interativa 🏅")
aba_geral, aba_pais = st.tabs(["🌍 Visão Global (Por Esporte)", "🔎 Raio-X Nacional (Por País e Atleta)"])

# --- ABA 1: VISÃO GLOBAL ---
with aba_geral:
    # Filtro específico da Aba 1
    modalidades_globais = sorted(df_ano['sport'].dropna().unique())
    mod_selecionada = st.selectbox("Selecione a Modalidade para analisar o mundo:", modalidades_globais, key='mod_global')
    
    df_mod = df_ano[df_ano['sport'] == mod_selecionada]
    
    col_mapa, col_rank = st.columns([3, 2])
    with col_mapa:
        fig_mapa = graf.plotar_mapa_mundi(df_mod)
        st.plotly_chart(fig_mapa, use_container_width=True)
    
    with col_rank:
        st.write("") 
        fig_rank = graf.plotar_ranking_top10(df_mod)
        st.pyplot(fig_rank)

# --- ABA 2: RAIO-X DO PAÍS (DRILL-DOWN DE ATLETAS) ---
with aba_pais:
    paises_medalhistas = sorted(df_ano['country'].dropna().unique())
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        # 1º Passo: Escolher o País
        pais_selecionado = st.selectbox("1. Selecione o País:", paises_medalhistas)
        df_pais = df_ano[df_ano['country'] == pais_selecionado]
        
    with col_f2:
        # 2º Passo: Escolher um esporte que ESSE país tem medalha
        mods_do_pais = sorted(df_pais['sport'].dropna().unique())
        mod_pais_selecionada = st.selectbox("2. Esporte com medalha (Filtra a Tabela abaixo):", mods_do_pais)
        
    # Aplicando o duplo filtro
    df_pais_mod = df_pais[df_pais['sport'] == mod_pais_selecionada]

    st.subheader(f"Indicadores Nacionais: {pais_selecionado}")
    dados_sociais = df_pais.iloc[0]
    
    c1, c2, c3, c4 = st.columns(4)
    # A métrica geral mostra o total do país na Olimpíada inteira
    c1.metric("🏅 Medalhas do País (Total)", df_pais.drop_duplicates(subset=['edition_id', 'event', 'medal']).shape[0])
    c2.metric("📊 IDH", round(dados_sociais['IDH'], 3) if pd.notna(dados_sociais['IDH']) else "N/A")
    c3.metric("👥 População", f"{dados_sociais['Population']:,.0f}".replace(',', '.') if pd.notna(dados_sociais['Population']) else "N/A")
    c4.metric("🌡️ Clima Médio", f"{dados_sociais['Clima_Medio']:.1f} °C" if pd.notna(dados_sociais['Clima_Medio']) else "N/A")
    
    st.divider()
    
    # Foco total no atleta individual do esporte selecionado
    col_tabela, col_biotipo = st.columns([1, 1])
    
    with col_tabela:
        st.subheader(f"Atletas de {mod_pais_selecionada}")
        df_tabela = df_pais_mod[['athlete', 'year', 'event', 'medal', 'height', 'weight']].drop_duplicates()
        df_tabela.columns = ['Nome', 'Ano', 'Categoria', 'Medalha', 'Altura(cm)', 'Peso(kg)']
        st.dataframe(df_tabela, use_container_width=True, hide_index=True)
        
    with col_biotipo:
        st.subheader("Perfil Físico dos Campeões")
        fig_biotipo = graf.plotar_biotipo_atletas(df_pais_mod)
        st.pyplot(fig_biotipo)