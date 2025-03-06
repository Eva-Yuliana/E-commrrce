import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi Tema
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title("📊 E-Commerce Interactive Dashboard")

# Load Dataset
@st.cache_data
def load_data():
    orders = pd.read_csv("D:\submission\data\orders_dataset.csv", parse_dates=["order_purchase_timestamp", "order_delivered_customer_date"])
    order_items = pd.read_csv("D:\submission\data\order_items_dataset.csv")
    products = pd.read_csv("D:\submission\data\products_dataset.csv")
    order_payments = pd.read_csv("D:\submission\data\order_payments_dataset.csv")

    # Data Processing
    orders["delivery_time"] = (orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]).dt.days
    order_items = order_items.merge(orders[["order_id", "delivery_time"]], on="order_id", how="left")
    order_items = order_items.merge(products, on="product_id", how="left")

    return orders, order_items, order_payments

orders, order_items, order_payments = load_data()

# Sidebar Filters
st.sidebar.header("🔎 Filter Data")

# Filter Rentang Harga
min_price, max_price = int(order_items["price"].min()), int(order_items["price"].max())
price_range = st.sidebar.slider("💰 Rentang Harga", min_value=min_price, max_value=max_price, value=(min_price, max_price))

# Filter Waktu Pengiriman
min_days, max_days = int(order_items["delivery_time"].min()), int(order_items["delivery_time"].max())
delivery_range = st.sidebar.slider("📦 Waktu Pengiriman (Hari)", min_value=min_days, max_value=max_days, value=(min_days, max_days))

# Filter Kategori Produk
categories = order_items["product_category_name"].dropna().unique()
selected_category = st.sidebar.multiselect("🛍️ Pilih Kategori Produk", options=categories, default=categories[:5])

# Menerapkan Filter
filtered_data = order_items[
    (order_items["price"] >= price_range[0]) & (order_items["price"] <= price_range[1]) &
    (order_items["delivery_time"] >= delivery_range[0]) & (order_items["delivery_time"] <= delivery_range[1]) &
    (order_items["product_category_name"].isin(selected_category))
]

# Layout 2 Kolom
col1, col2 = st.columns(2)

# Visualisasi 1: Korelasi Harga Produk dan Waktu Pengiriman
with col1:
    st.subheader("📈 Korelasi Harga & Waktu Pengiriman")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=filtered_data, x="price", y="delivery_time", alpha=0.7, ax=ax)
    st.pyplot(fig)

# Visualisasi 2: Distribusi Waktu Pengiriman
with col2:
    st.subheader("⏳ Distribusi Waktu Pengiriman")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(filtered_data["delivery_time"].dropna(), bins=30, kde=True, ax=ax, color="purple")
    st.pyplot(fig)

# Visualisasi 3: Kategori Produk Paling Populer
st.subheader("🛒 Kategori Produk yang Paling Banyak Dibeli")
top_categories = filtered_data["product_category_name"].value_counts().head(10)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=top_categories.values, y=top_categories.index, ax=ax, hue=top_categories.index, palette="coolwarm", legend=False)
st.pyplot(fig)

# Visualisasi 4: Metode Pembayaran yang Sering Digunakan
st.subheader("💳 Distribusi Metode Pembayaran")
fig, ax = plt.subplots(figsize=(10, 5))
sns.countplot(x=order_payments["payment_type"], hue=order_payments["payment_type"], order=order_payments["payment_type"].value_counts().index, ax=ax, palette="Blues", legend=False)
st.pyplot(fig)

st.sidebar.markdown("📌 **Gunakan filter untuk menyesuaikan tampilan dashboard!**")
