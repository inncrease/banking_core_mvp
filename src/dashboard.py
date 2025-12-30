import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px  # <--- New library for interactive charts

# --- CONFIGURATION ---
DB_NAME = "banking.db"

def get_connection():
    """Establishes a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)

# --- PAGE SETUP ---
st.set_page_config(page_title="Banking Core Dashboard", page_icon="🏦", layout="wide")

st.title("🏦 Banking Core Analytics")
st.markdown("Real-time overview of users, transactions, and financial health.")

# --- DATA LOADING ---
conn = get_connection()
df_users = pd.read_sql("SELECT * FROM users", conn)
df_transactions = pd.read_sql("SELECT * FROM transactions", conn)
conn.close()

# --- KPI METRICS ---
col1, col2, col3 = st.columns(3)

with col1:
    total_users = len(df_users)
    st.metric(label="Total Clients", value=total_users)

with col2:
    total_money = df_users["balance"].sum()
    st.metric(label="Total Liquidity", value=f"${total_money:,.2f}")

with col3:
    total_tx = len(df_transactions)
    st.metric(label="Total Transactions", value=total_tx)

st.divider()

# --- VISUALIZATION SECTION ---

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🍰 Wealth Distribution")
    
    # Check if we have data to plot
    if not df_users.empty:
        # Create a Pie Chart using Plotly
        # values = slice size (money), names = slice label (last name)
        fig = px.pie(
            df_users, 
            values='balance', 
            names='last_name', 
            title='Who holds the capital?',
            hole=0.4 # Makes it a Donut Chart (looks more modern)
        )
        # Display the interactive chart
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No users found.")

with col_right:
    st.subheader("📉 Transaction History (Last 10)")
    if not df_transactions.empty:
        latest_tx = df_transactions.sort_values(by="created_at", ascending=False).head(10)
        st.dataframe(latest_tx[["sender_id", "receiver_id", "amount", "created_at"]], hide_index=True)
    else:
        st.info("No transactions found yet.")

# --- REFRESH BUTTON ---
if st.sidebar.button("Refresh Data"):
    st.rerun()