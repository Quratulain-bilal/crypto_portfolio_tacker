import os
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import hashlib
from sklearn.linear_model import LinearRegression
import numpy as np

# ==================== Custom CSS for Styling ====================
def set_custom_css():
    css = """
     
    """
    st.markdown(css, unsafe_allow_html=True)

# ==================== File-Based Authentication ====================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists("users.csv"):
        pd.DataFrame(columns=["username", "password"]).to_csv("users.csv", index=False)
    return pd.read_csv("users.csv")

def save_user(username, hashed_password):
    users_df = load_users()
    new_user = pd.DataFrame({"username": [username], "password": [hashed_password]})
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv("users.csv", index=False)

def authenticate_user(username, password):
    users_df = load_users()
    hashed_password = hash_password(password)
    return not users_df[(users_df["username"] == username) & (users_df["password"] == hashed_password)].empty

# ==================== Fetch Crypto Price ====================
@st.cache_data(ttl=60)  # Cache results for 60 seconds
def fetch_crypto_price(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        if coin_id in data and "usd" in data[coin_id]:
            return data[coin_id]["usd"]
        else:
            st.error(f"No price data found for {coin_id}. Please try again later.")
            return None
    except Exception as e:
        st.error(f"Error fetching price for {coin_id}: {str(e)}")
        return None

# ==================== Fetch News ====================
@st.cache_data(ttl=3600)  # Cache results for 1 hour
def fetch_news(query):
    try:
        api_key = "e3bd6441ee034768805906521bb246e5"  # Replace with your actual NewsAPI key
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])
        return articles
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        return []

# ==================== Fetch Crypto Historical Data ====================
@st.cache_data(ttl=3600)  # Cache results for 1 hour
def fetch_crypto_historical_data(coin_id, days=30):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
        response = requests.get(url)
        data = response.json()
        prices = pd.DataFrame(data["prices"], columns=["Date", "Price"])
        prices["Date"] = pd.to_datetime(prices["Date"], unit="ms")
        return prices
    except Exception as e:
        st.error(f"Error fetching historical data for {coin_id}: {str(e)}")
        return None

# ==================== Predict Future Price ====================
def predict_future_price(historical_data):
    try:
        historical_data = historical_data.dropna()
        X = np.array(range(len(historical_data))).reshape(-1, 1)
        y = historical_data["Price"].values

        model = LinearRegression()
        model.fit(X, y)

        future_X = np.array(range(len(historical_data), len(historical_data) + 7)).reshape(-1, 1)
        future_prices = model.predict(future_X)

        last_date = historical_data["Date"].iloc[-1]
        future_dates = pd.date_range(start=last_date, periods=8)[1:]  # Exclude the first date (last_date)

        future_df = pd.DataFrame({"Date": future_dates, "Predicted Price": future_prices})
        return future_df
    except Exception as e:
        st.error(f"Error predicting future prices: {str(e)}")
        return None

# ==================== Configure the Streamlit App ====================
st.set_page_config(page_title="Crypto Portfolio Tracker", layout="wide")
set_custom_css()

# Sidebar for Login/Logout and Settings
st.sidebar.header("User Settings")
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.sidebar.title("🔒 Login / Signup")
    choice = st.sidebar.selectbox("Choose an option:", ["Login", "Signup"])

    username = st.sidebar.text_input("Trader Username")
    password = st.sidebar.text_input("Password", type="password")

    if choice == "Login":
        if st.sidebar.button("Login"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.success(f"Logged in as {username}")
                st.rerun()  # Refresh the app
            else:
                st.error("Invalid username or password.")
    elif choice == "Signup":
        if st.sidebar.button("Signup"):
            if username in load_users()["username"].values:
                st.error("Username already exists.")
            else:
                save_user(username, hash_password(password))
                st.success("Account created successfully!")
else:
    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ==================== Main App (After Login) ====================
if st.session_state.logged_in:
    st.title("📊 Crypto Portfolio Tracker")
    st.write("Track your investments across cryptocurrencies!")

    # Initialize session state for portfolio
    if 'portfolio' not in st.session_state or st.session_state.portfolio.empty:
        st.session_state.portfolio = pd.DataFrame(columns=["Asset", "Quantity", "Purchase Price", "Current Price"])

    # Add Assets to Portfolio
    with st.form("add_asset_form"):
        st.subheader("Add a Cryptocurrency to Your Portfolio")
        coin_id = st.selectbox("Select Cryptocurrency", [
            "bitcoin", "ethereum", "ripple", "cardano", "dogecoin",
            "binancecoin", "solana", "polkadot", "chainlink", "litecoin"
        ])
        current_price = fetch_crypto_price(coin_id)
        ticker = coin_id.capitalize()
        quantity = st.number_input("Quantity Purchased", min_value=1)
        purchase_price = st.number_input("Purchase Price ($)", min_value=0.01)
        submitted = st.form_submit_button("Add Asset")

        if submitted:
            if current_price is not None:
                new_asset = pd.DataFrame({
                    "Asset": [ticker],
                    "Quantity": [quantity],
                    "Purchase Price": [purchase_price],
                    "Current Price": [current_price]
                })
                st.session_state.portfolio = pd.concat([st.session_state.portfolio, new_asset], ignore_index=True)
                st.success(f"Added {ticker} to your portfolio!")
            else:
                st.error("Failed to fetch asset price. Please check the input.")

    # Display Portfolio
    if not st.session_state.portfolio.empty:
        st.subheader("Your Portfolio")
        st.session_state.portfolio["Total Investment"] = (
            st.session_state.portfolio["Quantity"] * st.session_state.portfolio["Purchase Price"]
        )
        st.session_state.portfolio["Current Value"] = (
            st.session_state.portfolio["Quantity"] * st.session_state.portfolio["Current Price"]
        )
        st.session_state.portfolio["Profit/Loss"] = (
            st.session_state.portfolio["Current Value"] - st.session_state.portfolio["Total Investment"]
        )

        st.dataframe(st.session_state.portfolio)

        # Delete Option
        st.subheader("Delete an Asset")
        asset_to_delete = st.selectbox("Select an Asset to Delete", st.session_state.portfolio["Asset"].unique())
        if st.button("Delete Asset"):
            st.session_state.portfolio = st.session_state.portfolio[
                st.session_state.portfolio["Asset"] != asset_to_delete
            ]
            st.success(f"Deleted {asset_to_delete} from your portfolio!")

        # Visualize Portfolio
        st.subheader("Portfolio Performance")

        # Pie chart for asset distribution
        fig_pie = px.pie(st.session_state.portfolio, values="Current Value", names="Asset", title="Portfolio Distribution")
        st.plotly_chart(fig_pie)

        # Bar chart for profit/loss
        fig_bar = px.bar(st.session_state.portfolio, x="Asset", y="Profit/Loss", title="Profit/Loss by Asset")
        st.plotly_chart(fig_bar)

        # Export Portfolio as CSV
        csv = st.session_state.portfolio.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Portfolio as CSV",
            data=csv,
            file_name="portfolio.csv",
            mime="text/csv"
        )

        # Latest News with Image
        st.subheader("Latest News")
        selected_crypto = st.selectbox("Select a Cryptocurrency for News", [
            "bitcoin", "ethereum", "ripple", "cardano", "dogecoin",
            "binancecoin", "solana", "polkadot", "chainlink", "litecoin"
        ])
        news_articles = fetch_news(selected_crypto)
        if news_articles:
            for article in news_articles[:5]:  # Show top 5 articles
                st.markdown(f"- [{article['title']}]({article['url']})")
        else:
            st.info("No news available at the moment.")

        # Add Image Related to News
        st.markdown("""
        <div style="display: flex; align-items: center;">
            <div style="flex: 1;">
                <img src="https://img.freepik.com/premium-psd/candlestick-chart-transparent-background_1059676-44474.jpg?w=1380" 
                     alt="News Chart" style="width: 100%; max-width: 300px; margin-right: 20px;">
            </div></div>
        """, unsafe_allow_html=True)

        # Backtesting
        st.subheader("Backtest Trading Strategy")
        historical_data = fetch_crypto_historical_data(selected_crypto, days=30)
        if historical_data is not None:
            st.write("Historical Data:")
            st.dataframe(historical_data)

            # Simple Moving Average Strategy
            historical_data["SMA_7"] = historical_data["Price"].rolling(window=7).mean()
            historical_data["Signal"] = (historical_data["Price"] > historical_data["SMA_7"]).astype(int)
            st.write("Backtest Results:")
            st.dataframe(historical_data)

            # Line Chart for Historical Data
            fig_backtest = px.line(historical_data, x="Date", y=["Price", "SMA_7"], title=f"{selected_crypto.capitalize()} Price with SMA")
            st.plotly_chart(fig_backtest)

        # Machine Learning Prediction with Image
        st.subheader("Future Price Prediction")
        future_prices = predict_future_price(historical_data)
        if future_prices is not None:
            st.write("Predicted Prices for Next 7 Days:")
            st.write(future_prices)

            # Add Image Related to Future Prediction
            st.markdown("""
            <div style="display: flex; align-items: center;">
                <div style="flex: 1;">
                    <img src="https://img.freepik.com/free-photo/people-tablet-with-bar-graph_1134-473.jpg?t=st=1740021379~exp=1740024979~hmac=ae0e8801abd9eddb7f8dc67dcea525bf403767f4a0d34fb8abd01255bf0ad3c8&w=996" 
                         alt="Prediction Chart" style="width: 100%; max-width: 900px; margin-right: 20px;">
                </div>
                </div>
            """, unsafe_allow_html=True)

    else:
        st.info("Your portfolio is empty. Add assets to get started!")

# Footer
st.markdown("""
© 2023 Crypto Portfolio Tracker
""", unsafe_allow_html=True)
