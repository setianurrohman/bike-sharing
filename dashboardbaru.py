import streamlit as st
import pandas as pd
import plotly.express as px

# ===== CONFIG =====
st.set_page_config(page_title="Bike Dashboard", page_icon="🚲", layout="wide")

# ===== SESSION LOGIN =====
if "login" not in st.session_state:
    st.session_state.login = False

# ===== LOGIN PAGE =====
if not st.session_state.login:
    st.markdown("<h1 style='text-align:center;'>🚲 BIKE CYCLE : Bike Sharing Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Masukkan nama untuk masuk</h3>", unsafe_allow_html=True)

    name = st.text_input("Nama kamu")

    if st.button("Masuk"):
        if name != "":
            st.session_state.login = True
            st.session_state.user = name
            st.rerun()
        else:
            st.warning("Isi nama dulu!")

    st.stop()

# ===== STYLE =====
st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
@st.cache_data
def load_data():
    day = pd.read_csv("day.csv", sep=";")
    hour = pd.read_csv("hour.csv", sep=";")
    season_map= {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
    }
    day['season'] = day['season'].map(season_map)
    years_map= {
    0: 2011,
    1: 2012
    }
    day['yr'] = day['yr'].map(years_map)

    day.columns = day.columns.str.strip()
    hour.columns = hour.columns.str.strip()

    day['dteday'] = pd.to_datetime(day['dteday'],format="%d/%m/%Y")
    hour['dteday'] = pd.to_datetime(hour['dteday'],format="%d/%m/%Y")

    return day, hour

day_df, hour_df = load_data()

# ===== SIDEBAR =====
st.sidebar.title(f"👋 Halo, {st.session_state.user}")

menu_list = [
    "🏠 Home",
    "📈 Per Bulan",
    "⏰ Per Jam",
    "📊 Hari Kerja vs Libur",
    "🌦️ Musim",
    "📄 Data"
]

# default menu
if "menu" not in st.session_state:
    st.session_state.menu = "🏠 Home"

st.sidebar.title("📂 Menu")

for item in menu_list:
    if st.sidebar.button(item, use_container_width=True):
        st.session_state.menu = item

menu = st.session_state.menu

st.markdown("""
<style>
div.stButton > button {
    text-align: left;
    padding: 12px 20px;
    margin-bottom: 5px;
    border-radius: 12px;
    background-color: #1f2937;
    color: gold;
    border: none;
    font-size: 18px;
}
div.stButton > button:hover {
    background-color: #374151;
    transform: translateX(5px);
}
</style>
""", unsafe_allow_html=True)

# ===== HOME =====
if menu == "🏠 Home":
    st.title("🚲 BIKE CYCLE")
    st.markdown("### Dashboard Analisis Tren Penggunaan Sepeda Berdasarkan Waktu")

    st.image("assets/fotohome.jpeg", use_container_width=True)

# ===== PER BULAN =====
elif menu == "📈 Per Bulan":
    st.title("📈 Penggunaan Sepeda per Bulan")

    tahun = st.selectbox("Pilih Tahun", [2011, 2012])
    df = day_df[day_df['yr'] == tahun]

    monthly = df.resample('ME', on='dteday')['cnt'].mean().reset_index()
    monthly['bulan'] = monthly['dteday'].dt.strftime('%b %Y')

    fig = px.line(monthly, x='bulan', y='cnt', markers=True, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# ===== PER JAM =====
elif menu == "⏰ Per Jam":
    st.title("⏰ Penggunaan per Jam")

    hourly = hour_df.groupby('hr')['cnt'].mean().reset_index()

    fig = px.line(hourly, x='hr', y='cnt', markers=True, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# ===== HARI KERJA =====
elif menu == "📊 Hari Kerja vs Libur":
    st.title("📊 Perbandingan Hari Kerja")

    df = day_df.groupby('workingday')['cnt'].mean().reset_index()

    fig = px.bar(df, x='workingday', y='cnt', color='workingday', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# ===== MUSIM =====
elif menu == "🌦️ Musim":
    st.title("🌦️ Musim Paling Ramai")

    df = day_df.groupby('season')['cnt'].mean().reset_index()

    fig = px.bar(df, x='season', y='cnt', color='season', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# ===== DATA =====
elif menu == "📄 Data":
    st.title("📄 Data")
    st.dataframe(day_df, use_container_width=True)
    st.dataframe(hour_df, use_container_width=True)
