import streamlit as st
import plotly.express as px
from utils.data_loader import fetch_rss_data

st.set_page_config(page_title="Social Trend & Sentiment Analysis", page_icon="📈", layout="wide")

st.title("📈 Social Media Trend & Sentiment Dashboard")
st.caption("Monitoraggio del sentiment tramite VADER, LLM (Gemini) e Feed RSS.")

# --- PARAMETRI IN BASE ALLA FONTE SELEZIONATA ---
if source_type == "Reddit API":
    st.sidebar.subheader("Credenziali Reddit")
    topic = st.sidebar.text_input("Argomento / Hashtag da tracciare", value="Technology")
    client_id = st.sidebar.text_input("Reddit Client ID", type="password")
    client_secret = st.sidebar.text_input("Reddit Client Secret", type="password")
else:
    st.sidebar.subheader("Seleziona Feed RSS")
    
    # Dizionario delle fonti predefinite
    rss_options = {
        "La Gazzetta del Mezzogiorno": "https://feeds.feedburner.com/lagazzettadelmezzogiorno/viyi6z8dkwu",
        "La Gazzetta dello Sport - Calcio": "https://www.gazzetta.it/dynamic-feed/rss/section/Calcio.xml",
        "Google News Technology": "https://news.google.com/rss/search?q=technology&hl=it&gl=IT&ceid=IT:it",
        "URL Personalizzato": "custom"
    }
    
    selected_feed_label = st.sidebar.selectbox(
        "Scegli una fonte RSS predefinita:",
        list(rss_options.keys())
    )
    
    if rss_options[selected_feed_label] == "custom":
        rss_url = st.sidebar.text_input("Inserisci URL Feed RSS personalizzato:")
    else:
        rss_url = rss_options[selected_feed_label]

# --- Load Data ---
with st.spinner("Estrazione dati e calcolo sentiment in corso..."):
    df = fetch_rss_data(rss_url, engine=engine, api_key=gemini_key)

if not df.empty:
    # --- KPI Top ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Notizie/Post Analizzati", len(df))
    c2.metric("Like Totali Stimati", f"{df['likes'].sum():,}")
    pos_pct = (len(df[df['sentiment_category'] == 'Positivo']) / len(df)) * 100
    c3.metric("% Sentiment Positivo", f"{pos_pct:.1f}%")
    neg_pct = (len(df[df['sentiment_category'] == 'Negativo']) / len(df)) * 100
    c4.metric("% Sentiment Negativo", f"{neg_pct:.1f}%")

    st.divider()

    # --- Charts ---
    col_chart1, col_chart2 = st.columns(2)
    color_map = {'Positivo': '#2ecc71', 'Neutro': '#95a5a6', 'Negativo': '#e74c3c'}

    with col_chart1:
        st.subheader("Ripartizione Sentiment")
        fig_pie = px.pie(df, names='sentiment_category', color='sentiment_category', color_discrete_map=color_map, hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_chart2:
        st.subheader("Volume Post / Sentiment")
        fig_bar = px.histogram(df, x='sentiment_category', color='sentiment_category', color_discrete_map=color_map)
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- Data Table ---
    st.subheader("Feed Analizzato")
    st.dataframe(df[['timestamp', 'post', 'likes', 'shares', 'sentiment_category']], use_container_width=True, hide_index=True)
else:
    st.warning("Nessun dato trovato per l'URL inserito.")