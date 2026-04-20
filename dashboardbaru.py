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
    "💎 Distribusi Data",
    "🎲 Hubungan Variabel",
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

# ===== DISTRIBUSI DATA ====
elif menu == "💎 Distribusi Data":
    st.title("Distribusi Penggunaan Sepeda")

    # Histogram
    fig1 = px.histogram(day_df, x="cnt", title="Distribusi Jumlah Pengguna Sepeda")
    fig1.update_layout(xaxis_title="Jumlah Pengguna", yaxis_title="Frekuensi")
    st.plotly_chart(fig1)

    st.write("Sebagian besar penggunaan sepeda berada di tingkat menengah, dengan beberapa lonjakan tinggi.")

    # Boxplot
    fig2 = px.box(day_df, x="cnt", title="Boxplot Pengguna Sepeda")
    fig2.update_layout(xaxis_title="Jumlah Pengguna")
    st.plotly_chart(fig2)

    st.write("Terlihat adanya outlier, yaitu hari dengan jumlah pengguna yang sangat tinggi.")

# ==== HUBUNGAN ====
elif menu == "🎲 Hubungan Variabel":
    st.title("Hubungan Antar Variabel")

    # Scatter + garis tren
    fig3 = px.scatter(day_df, x="temp", y="cnt",
                      title="Hubungan Temperatur dengan Pengguna Sepeda")
    fig3.update_layout(xaxis_title="Temperatur", yaxis_title="Jumlah Pengguna")
    st.plotly_chart(fig3)

    st.write("Semakin tinggi temperatur, jumlah pengguna sepeda cenderung meningkat.")

    # Correlation Heatmap
    corr = day_df[['cnt','temp','hum','windspeed']].corr()

    fig4 = px.imshow(corr, text_auto=True, title="Correlation Matrix")
    st.plotly_chart(fig4)

    st.write("Temperatur memiliki hubungan paling kuat dengan jumlah pengguna sepeda.")

# ===== DATA =====
elif menu == "📄 Data":
    st.title("📄 Data")
    st.dataframe(day_df, use_container_width=True)
    st.dataframe(hour_df, use_container_width=True)
