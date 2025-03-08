import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 1rem;
    }
    .title-text {
        font-size: 40px !important;
        text-align: center;
        color: #2C3E50;
        padding: 20px;
    }
    .subtitle-text {
        font-size: 20px !important;
        text-align: center;
        color: #7F8C8D;
        margin-bottom: 30px;
    }
    .stPlotlyChart {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# === 1. Load Dataset ===
@st.cache_data
def load_data():
    # Load cleaned data
    df = pd.read_csv("dashboard/cleaned_data.csv", parse_dates=["order_purchase_timestamp"])
    return df

df = load_data()

# === 2. Dashboard Title ===
st.markdown("<h1 class='title-text'>📊 E-Commerce Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>Analisis Data Pesanan, Pembayaran, dan Produk</p>", unsafe_allow_html=True)

# === 3. Layout dengan Columns ===
col1, col2 = st.columns([2, 1])

with col2:
    # Features Section
    st.sidebar.header("🎯 Fitur Dashboard")
    st.sidebar.markdown("""
    - 📊 **Visualisasi Interaktif**
    - 📅 **Filter Data berdasarkan Tanggal**
    - 📈 **Analisis Tren Penjualan**
    - 💳 **Analisis Metode Pembayaran**
    - 🛍️ **Analisis Kategori Produk**
    - 📋 **Tabel Data Transaksi**
    """)
    
    st.sidebar.markdown("---")
    
    # Filter Data Section
    st.sidebar.header("📅 Filter Data")
    date_range = st.sidebar.date_input(
        "Pilih Rentang Waktu",
        [df['order_purchase_timestamp'].min(), df['order_purchase_timestamp'].max()]
    )
    
    # Informasi Dataset
    st.sidebar.markdown("---")
    st.sidebar.header("ℹ️ Informasi Dataset")
    st.sidebar.write(f"Total Transaksi: {len(df):,}")
    st.sidebar.write(f"Total Pembayaran: ${df['payment_value'].sum():,.2f}")
    st.sidebar.write(f"Rata-rata Nilai Transaksi: ${df['payment_value'].mean():,.2f}")

filtered_df = df[(df['order_purchase_timestamp'] >= pd.to_datetime(date_range[0])) & 
                 (df['order_purchase_timestamp'] <= pd.to_datetime(date_range[1]))]

# === 4. Create Tabs ===
tab1, tab2, tab3, tab4 = st.tabs(["📈 Tren Pesanan", "💳 Metode Pembayaran", "🛍️ Kategori Produk", "📋 Data Transaksi"])

# Tab 1: Tren Pesanan
with tab1:
    st.subheader("📈 Tren Jumlah Pesanan per Bulan")
    # Format the month-year display
    df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M')
    monthly_orders = df.groupby('order_month').size().reset_index()
    monthly_orders['month_year'] = monthly_orders['order_month'].apply(lambda x: x.strftime('%B %Y'))
    monthly_orders['order_month'] = monthly_orders['order_month'].astype(str)

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    sns.lineplot(data=monthly_orders, x='month_year', y=0, marker='o', 
                color='#2E86C1', linewidth=2, markersize=8)
    
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Bulan", fontsize=12, fontweight='bold')
    plt.ylabel("Jumlah Pesanan", fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.title("Tren Pesanan Bulanan", pad=20, fontsize=14, fontweight='bold')
    plt.tight_layout()

    max_point = monthly_orders[monthly_orders[0] == monthly_orders[0].max()]
    min_point = monthly_orders[monthly_orders[0] == monthly_orders[0].min()]

    plt.annotate(f'Max: {int(max_point[0].iloc[0])}',
                xy=(list(monthly_orders['month_year']).index(max_point['month_year'].iloc[0]), max_point[0].iloc[0]),
                xytext=(10, 10), textcoords='offset points')
    
    plt.annotate(f'Min: {int(min_point[0].iloc[0])}',
                xy=(list(monthly_orders['month_year']).index(min_point['month_year'].iloc[0]), min_point[0].iloc[0]),
                xytext=(10, -15), textcoords='offset points')

    st.pyplot(fig)

    # Informasi Statistik
    st.write("Informasi Statistik:")
    st.write(f"- Periode data: {monthly_orders['month_year'].iloc[0]} hingga {monthly_orders['month_year'].iloc[-1]}")
    st.write(f"- Jumlah pesanan tertinggi: {int(max_point[0].iloc[0])} ({max_point['month_year'].iloc[0]})")
    st.write(f"- Jumlah pesanan terendah: {int(min_point[0].iloc[0])} ({min_point['month_year'].iloc[0]})")

# Tab 2: Metode Pembayaran
with tab2:
    st.subheader("💳 Distribusi Metode Pembayaran")
    payment_counts = filtered_df['payment_type'].value_counts()
    
    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#2E86C1', '#E74C3C', '#27AE60', '#F1C40F']
    sns.barplot(x=payment_counts.index, y=payment_counts.values, 
                palette=colors, ax=ax)
    plt.xticks(rotation=30)
    plt.xlabel("Metode Pembayaran", fontsize=12, fontweight='bold')
    plt.ylabel("Jumlah Transaksi", fontsize=12, fontweight='bold')
    plt.title("Distribusi Metode Pembayaran", pad=20, fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    
    # Informasi Statistik
    st.write("Informasi Metode Pembayaran:")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Jumlah transaksi per metode pembayaran:")
        for payment_type, count in payment_counts.items():
            st.write(f"- {payment_type}: {count:,} transaksi")
    with col2:
        st.write("Persentase penggunaan:")
        for payment_type, count in payment_counts.items():
            percentage = (count / len(filtered_df)) * 100
            st.write(f"- {payment_type}: {percentage:.1f}%")

# Tab 3: Kategori Produk
with tab3:
    col1, col2 = st.columns([2, 1])
    with col2:
        n_categories = st.slider("Jumlah Kategori", min_value=5, max_value=20, value=10)
        chart_type = st.radio("Tipe Chart", ["Bar", "Horizontal Bar"])
    
    st.subheader(f"🛍️ Top {n_categories} Kategori Produk Terlaris")
    top_categories = filtered_df['product_category_name_x'].value_counts().head(n_categories)
    
    # Visualisasi
    colors = sns.color_palette("magma", n_colors=n_categories)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if chart_type == "Bar":
        sns.barplot(x=top_categories.values, y=top_categories.index, 
                    palette=colors, ax=ax)
        plt.xlabel("Jumlah Pesanan", fontsize=12, fontweight='bold')
        plt.ylabel("Kategori Produk", fontsize=12, fontweight='bold')
    else:
        sns.barplot(y=top_categories.values, x=top_categories.index, 
                    palette=colors, ax=ax)
        plt.ylabel("Jumlah Pesanan", fontsize=12, fontweight='bold')
        plt.xlabel("Kategori Produk", fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        # Adjust layout to prevent text overlap
        plt.subplots_adjust(bottom=0.2)  # Add more space at the bottom
    
    plt.title(f"Top {n_categories} Kategori Produk Terlaris", pad=20, fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    
    # Informasi Statistik
    st.write("Informasi Kategori Produk:")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Top 5 kategori dengan penjualan tertinggi:")
        for cat, count in top_categories.head().items():
            st.write(f"- {cat}: {count:,} pesanan")
    with col2:
        total_products = len(filtered_df)
        st.write("Persentase dari total pesanan:")
        for cat, count in top_categories.head().items():
            percentage = (count / total_products) * 100
            st.write(f"- {cat}: {percentage:.1f}%")

# Tab 4: Data Transaksi
with tab4:
    st.subheader("📋 Data Transaksi Terbaru")
    
    # Tampilkan statistik ringkas
    st.write("Ringkasan Transaksi:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Transaksi", f"{len(filtered_df):,}")
    with col2:
        avg_value = filtered_df['payment_value'].mean()
        st.metric("Rata-rata Nilai Transaksi", f"${avg_value:,.2f}")
    with col3:
        total_value = filtered_df['payment_value'].sum()
        st.metric("Total Nilai Transaksi", f"${total_value:,.2f}")
    
    st.markdown("---")
    
    # Tampilkan tabel data
    st.write("10 Transaksi Terbaru:")
    st.dataframe(
        filtered_df[['order_id', 'product_category_name_x', 'payment_type', 
                    'price', 'payment_value', 'order_purchase_timestamp']]
        .head(10)
        .style.background_gradient(cmap='Blues', subset=['payment_value'])
        .format({'price': '${:.2f}', 'payment_value': '${:.2f}'})
    )
