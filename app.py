import os
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import hashlib
from sklearn.linear_model import LinearRegression
import numpy as np

# ==================== Multi-Language Support ====================
LANGUAGES = {
    "en": {  # English
        "login": "Login",
        "signup": "Signup",
        "logout": "Logout",
        "portfolio": "Portfolio",
        "add_asset": "Add Asset",
        "delete_asset": "Delete Asset",
        "news": "Latest News",
        "backtest": "Backtest Strategy",
        "predict": "Predict Future Price",
        "password": "Password",
        "username": "Username",
        "empty_portfolio": "Your portfolio is empty. Add assets to get started!",
        "profit_loss": "Profit/Loss by Asset",
        "distribution": "Portfolio Distribution",
        "download_csv": "Download Portfolio as CSV",
        "no_news": "No news available at the moment.",
        "backtest_results": "Backtest Results",
        "future_prices": "Predicted Prices for Next 7 Days",
    },
    "ur": {  # Urdu
        "login": "لاگ ان",
        "signup": "سائن اپ",
        "logout": "لاگ آؤٹ",
        "portfolio": "پورٹ فولیو",
        "add_asset": "ایسٹ شامل کریں",
        "delete_asset": "ایسٹ حذف کریں",
        "news": "تازہ ترین خبریں",
        "backtest": "رجحان کی جانچ پڑتال",
        "predict": "مستقبل کی قیمت پیش گوئی",
        "password": "پاس ورڈ",
        "username": "صارف نام",
        "empty_portfolio": "آپ کا پورٹ فولیو خالی ہے۔ شروع کرنے کے لیے ایسٹ شامل کریں!",
        "profit_loss": "نمائش/نقصان بلحاظ ایسٹ",
        "distribution": "پورٹ فولیو کی تقسیم",
        "download_csv": "پورٹ فولیو ڈاؤنلوڈ کریں (CSV)",
        "no_news": "ابھی کوئی خبر دستیاب نہیں ہے۔",
        "backtest_results": "رجحان کی جانچ پڑتال کے نتائج",
        "future_prices": "اگلے 7 دنوں کی قیمتیں پیش گوئی",
    },
    "nl": {  # Dutch
        "login": "Inloggen",
        "signup": "Registreren",
        "logout": "Uitloggen",
        "portfolio": "Portefeuille",
        "add_asset": "Actief Toevoegen",
        "delete_asset": "Actief Verwijderen",
        "news": "Laatste Nieuws",
        "backtest": "Strategie Backtesten",
        "predict": "Voorspel Toekomstige Prijs",
        "password": "Wachtwoord",
        "username": "Gebruikersnaam",
        "empty_portfolio": "Je portefeuille is leeg. Voeg activa toe om te beginnen!",
        "profit_loss": "Winst/Verlies per Actief",
        "distribution": "Portefeuilleverdeling",
        "download_csv": "Portefeuille Downloaden als CSV",
        "no_news": "Op dit moment geen nieuws beschikbaar.",
        "backtest_results": "Backtest Resultaten",
        "future_prices": "Voorspelde Prijzen voor de Komende 7 Dagen",
    },
}

if 'language' not in st.session_state:
    st.session_state.language = "en"

def translate(key):
    return LANGUAGES[st.session_state.language].get(key, key)

# ==================== Custom CSS for Styling ====================
def set_custom_css():
    css = """
    <style>
        /* General Styling */
        body { background-color: #121212; color: #ffffff; }
        .stButton>button { background-color: #bb86fc; color: #000000; border-radius: 5px; }
        .stTextInput>div>input { background-color: #1e1e1e; color: #ffffff; border-radius: 5px; padding: 10px; }
        .sidebar .sidebar-content { background-color: #1e1e1e; color: #ffffff; }
        h1, h2, h3, h4, h5, h6 { color: #bb86fc; }
        .stMarkdown p { color: #ffffff; }
        .stDataFrame { background-color: #1e1e1e; color: #ffffff; }
        img { border-radius: 10px; }

        /* Reduce White Space */
        .block-container { padding-top: 1rem; padding-bottom: 1rem; }
        .stPlotlyChart { margin-top: 1rem; margin-bottom: 1rem; }

        /* Backtesting and Prediction Sections */
        .backtesting-section, .prediction-section {
            background-color: #1e1e1e;
            border: 1px solid #bb86fc;
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1rem;
        }

        /* News Section */
        .news-section {
            background-color: #1e1e1e;
            border: 1px solid #bb86fc;
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1rem;
        }
    </style>
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
st.sidebar.header(translate("username"))
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Language Selector
language = st.sidebar.selectbox(translate("language"), ["English", "Urdu", "Dutch"])
if language == "English":
    st.session_state.language = "en"
elif language == "Urdu":
    st.session_state.language = "ur"
elif language == "Dutch":
    st.session_state.language = "nl"

if not st.session_state.logged_in:
    st.sidebar.title(f"🔒 {translate('login')} / {translate('signup')}")
    choice = st.sidebar.selectbox("Choose an option:", [translate("login"), translate("signup")])

    username = st.sidebar.text_input(translate("username"))
    password = st.sidebar.text_input(translate("password"), type="password")

    if choice == translate("login"):
        if st.sidebar.button(translate("login")):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.success(f"Logged in as {username}")
                st.rerun()  # Refresh the app
            else:
                st.error("Invalid username or password.")
    elif choice == translate("signup"):
        if st.sidebar.button(translate("signup")):
            if username in load_users()["username"].values:
                st.error("Username already exists.")
            else:
                save_user(username, hash_password(password))
                st.success("Account created successfully!")
else:
    # Logout Button
    if st.sidebar.button(translate("logout")):
        st.session_state.logged_in = False
        st.rerun()

# ==================== Main App (After Login) ====================
if st.session_state.logged_in:
    st.title(f"📊 {translate('portfolio')}")
    st.write("Track your investments across cryptocurrencies!")

    # Initialize session state for portfolio
    if 'portfolio' not in st.session_state or st.session_state.portfolio.empty:
        st.session_state.portfolio = pd.DataFrame(columns=["Asset", "Quantity", "Purchase Price", "Current Price"])

    # Add Assets to Portfolio
    with st.form("add_asset_form"):
        st.subheader(translate("add_asset"))
        coin_id = st.selectbox("Select Cryptocurrency", [
            "bitcoin", "ethereum", "ripple", "cardano", "dogecoin",
            "binancecoin", "solana", "polkadot", "chainlink", "litecoin"
        ])
        current_price = fetch_crypto_price(coin_id)
        ticker = coin_id.capitalize()
        quantity = st.number_input("Quantity Purchased", min_value=1)
        purchase_price = st.number_input("Purchase Price ($)", min_value=0.01)
        submitted = st.form_submit_button(translate("add_asset"))

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
        st.subheader(translate("portfolio"))
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
        st.subheader(translate("delete_asset"))
        asset_to_delete = st.selectbox("Select an Asset to Delete", st.session_state.portfolio["Asset"].unique())
        if st.button(translate("delete_asset")):
            st.session_state.portfolio = st.session_state.portfolio[
                st.session_state.portfolio["Asset"] != asset_to_delete
            ]
            st.success(f"Deleted {asset_to_delete} from your portfolio!")

        # Visualize Portfolio
        st.subheader("Portfolio Performance")

        # Pie chart for asset distribution
        fig_pie = px.pie(st.session_state.portfolio, values="Current Value", names="Asset", title=translate("distribution"))
        st.plotly_chart(fig_pie)

        # Bar chart for profit/loss
        fig_bar = px.bar(st.session_state.portfolio, x="Asset", y="Profit/Loss", title=translate("profit_loss"))
        st.plotly_chart(fig_bar)

        # Export Portfolio as CSV
        csv = st.session_state.portfolio.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=translate("download_csv"),
            data=csv,
            file_name="portfolio.csv",
            mime="text/csv"
        )

        # Latest News with Image
        st.subheader(translate("news"))
        selected_crypto = st.selectbox("Select a Cryptocurrency for News", [
            "bitcoin", "ethereum", "ripple", "cardano", "dogecoin",
            "binancecoin", "solana", "polkadot", "chainlink", "litecoin"
        ])
        news_articles = fetch_news(selected_crypto)
        if news_articles:
            for article in news_articles[:5]:  # Show top 5 articles
                st.markdown(f"- [{article['title']}]({article['url']})")
        else:
            st.info(translate("no_news"))

        # Add Image Related to News
        st.image(
            "https://img.freepik.com/premium-psd/candlestick-chart-transparent-background_1059676-44474.jpg?w=1380",
            caption="Cryptocurrency Trends",
            use_container_width=True
        )

        # Backtesting Section
        st.markdown('<div class="backtesting-section">', unsafe_allow_html=True)
        st.subheader(translate("backtest"))
        historical_data = fetch_crypto_historical_data(selected_crypto, days=30)
        if historical_data is not None:
            st.write("Historical Data:")
            st.dataframe(historical_data)

            # Simple Moving Average Strategy
            historical_data["SMA_7"] = historical_data["Price"].rolling(window=7).mean()
            historical_data["Signal"] = (historical_data["Price"] > historical_data["SMA_7"]).astype(int)
            st.write(translate("backtest_results"))
            st.dataframe(historical_data)

            # Line Chart for Historical Data
            fig_backtest = px.line(historical_data, x="Date", y=["Price", "SMA_7"], title=f"{selected_crypto.capitalize()} Price with SMA")
            st.plotly_chart(fig_backtest)

            # Add Image for Backtesting
            st.image(
                "https://img.freepik.com/free-photo/businessman-hand-touching-stock-market-graph-on-virtual-screen-financial-trading-investment-concept_53876-129748.jpg?w=1380",
                caption="Backtesting Visualization",
                use_container_width=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Machine Learning Prediction Section
        st.markdown('<div class="prediction-section">', unsafe_allow_html=True)
        st.subheader(translate("predict"))
        future_prices = predict_future_price(historical_data)
        if future_prices is not None:
            st.write(translate("future_prices"))
            st.write(future_prices)

            # Add Image for Future Prediction
            st.image(
                "https://img.freepik.com/free-photo/people-tablet-with-bar-graph_1134-473.jpg?t=st=1740021379~exp=1740024979~hmac=ae0e8801abd9eddb7f8dc67dcea525bf403767f4a0d34fb8abd01255bf0ad3c8&w=996",
                caption="Future Trends",
                use_container_width=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("⚠️ Your portfolio is empty. Add assets to get started!")
