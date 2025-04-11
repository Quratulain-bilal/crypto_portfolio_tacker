📈 Crypto Portfolio Tracker
A multi-language crypto portfolio tracking web app built with Streamlit, allowing users to:

Track cryptocurrency investments

Predict future prices

View crypto-related news

Backtest strategies

Secure login/signup (file-based authentication)

Choose UI language: 🇬🇧 English | 🇵🇰 Urdu | 🇳🇱 Dutch

🚀 Features
🔒 Authentication System – Signup/Login with secure password hashing

🌐 Multi-language Interface – English, Urdu, and Dutch translations

📉 Portfolio Tracking – Add/delete crypto assets and track profit/loss

📊 Visualizations – Plotly charts for performance and distribution

📰 Latest News – Get live crypto news using NewsAPI

🔮 Price Prediction – Predict prices for the next 7 days using Linear Regression

🔁 Backtesting – View historical performance of assets

📥 CSV Download – Export your portfolio in .csv format

🎨 Custom Dark Theme – Stylish, responsive UI with minimal white space

🛠️ Tech Stack
Python

Streamlit

Pandas, NumPy, Scikit-learn

Plotly

Requests, hashlib

NewsAPI, CoinGecko API

🧰 Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com//crypto-portfolio-tracker.git
cd crypto-portfolio-tracker
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the app:

bash
Copy
Edit
streamlit run app.py
🔑 API Keys
Replace api_key in the fetch_news() function with your own key from NewsAPI.org.

📁 Folder Structure
bash
Copy
Edit
crypto-portfolio-tracker/
│
├── app.py               # Main Streamlit app
├── users.csv            # File-based user storage
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
💬 Multi-Language Support
Use the sidebar to switch between languages. App supports:

English (en)

Urdu (ur)

Dutch (nl)

📌 Note
This app is built for educational/demo purposes.

Prices are fetched using the free CoinGecko API (60s cache).

Prediction is a basic linear regression model for demonstration.

🙌 Acknowledgements
Streamlit

NewsAPI

CoinGecko API

