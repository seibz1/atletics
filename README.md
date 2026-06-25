# 🏅 Dashboard Olímpico Avançado: Análise de Eficiência Esportiva

Este projeto é uma ferramenta de pesquisa de dados interativa desenvolvida em Python. O objetivo principal é investigar o impacto do poder econômico (PIB/IDH), tamanho da população, clima e características físicas (biotipo) no sucesso de nações nos Jogos Olímpicos.

O dashboard permite identificar padrões de "eficiência esportiva", mapeando quais países conseguem formar atletas de elite e dominar modalidades específicas mesmo possuindo recursos financeiros limitados.

## 🚀 Funcionalidades

A aplicação é dividida em dois eixos principais de pesquisa:

* **🌍 Visão Global (Por Esporte):** * Mapeamento geoespacial da densidade de medalhas através de um **Globo 3D interativo**.
    * Ranking de quantificação de hegemonia esportiva (Top 10 Países).
* **📊 Raio-X Nacional (Drill-Down Socioeconômico e Biométrico):**
    * Painel de KPIs socioeconômicos (Total de Medalhas, IDH, População e Clima Médio do país selecionado).
    * Gráfico de Dispersão (Peso x Altura) que revela o rigor físico exigido pela modalidade e traça o perfil corporal dos campeões.
    * Tabela de microdados dos atletas medalhistas.

## 🏗️ Arquitetura do Sistema

O software foi construído utilizando a **Arquitetura em Camadas (Layered Architecture)** para garantir a modularidade e facilitar a manutenção:

* `dados/`: Camada de Acesso a Dados (Arquivos CSV brutos).
* `processamento_dados.py`: Camada de Lógica de Negócio (Tratamento, limpeza, merges e engenharia de dados usando Pandas e Numpy).
* `graficos.py` e `app.py`: Camada de Apresentação (Interface visual e plotagem de gráficos com Streamlit, Matplotlib e Plotly).

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Manipulação de Dados:** Pandas, Numpy
* **Visualização de Dados:** Matplotlib, Plotly
* **Interface Web:** Streamlit

## ⚙️ Como executar o projeto localmente

Siga os passos abaixo para rodar a aplicação na sua máquina:

1.  Clone este repositório:
    ```bash
    git clone [https://github.com/seibz1/atletics.git](https://github.com/seibz1/atletics.git)
    ```

2.  Acesse a pasta do projeto:
    ```bash
    cd atletics
    ```

3.  Instale as dependências necessárias:
    ```bash
    pip install streamlit pandas numpy matplotlib plotly
    ```

4.  Execute o painel do Streamlit:
    ```bash
    streamlit run app.py
    ```

5.  O painel abrirá automaticamente no seu navegador no endereço: `http://localhost:8501`.