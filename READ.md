Crypto Portfolio Tracker Overview The Crypto Portfolio Tracker is a Streamlit-based web application designed to help cryptocurrency investors track their investments, analyze portfolio performance, and stay updated with the latest news and trends in the crypto market. The app provides a user-friendly interface with features like portfolio management, live price tracking, historical data analysis, machine learning-based price predictions, and more.

Features

User Authentication Login/Signup : Users can create an account or log in securely using file-based authentication. Session Management : The app uses st.session_state to maintain user sessions and ensure a seamless experience.
Portfolio Management Add Assets : Users can add cryptocurrencies to their portfolio by selecting from a predefined list (e.g., Bitcoin, Ethereum, etc.) and entering purchase details. View Portfolio : Displays the current portfolio with metrics like total investment, current value, and profit/loss. Delete Assets : Users can remove assets from their portfolio. Export Portfolio : Export the portfolio as a CSV file for offline use.
Portfolio Visualization Pie Chart : Visualizes the distribution of assets in the portfolio. Bar Chart : Displays profit/loss for each asset.
Live Price Tracking Fetches real-time cryptocurrency prices using the CoinGecko API . Provides live charts for selected cryptocurrencies using TradingView widgets.
News Feed Fetches the latest cryptocurrency-related news using the NewsAPI . Displays top 5 articles with clickable links.
Backtesting Allows users to backtest trading strategies using historical data. Implements a simple moving average (SMA) strategy to generate buy/sell signals.
Machine Learning Predictions Uses linear regression to predict future cryptocurrency prices for the next 7 days. Displays predicted prices alongside a visual chart.
Equality Curve Tracks the growth of the user's portfolio over time by plotting an equality curve.
Email Alerts (Placeholder) Includes a toggle in the sidebar to enable/disable email alerts for portfolio updates (placeholder functionality).
Custom Styling A visually appealing design with custom CSS for styling the navbar, sidebar, buttons, and footer. Dark mode toggle for better accessibility. How It Works
Setup Clone the repository: bash Copy 1 git clone https://github.com/your-repo/crypto-portfolio-tracker.git Install dependencies: bash Copy 1 pip install -r requirements.txt Run the app: bash Copy 1 streamlit run app.py
User Flow Authentication : New users can sign up by providing a username and password. Existing users can log in to access their portfolios. Portfolio Management : Add cryptocurrencies to the portfolio by selecting the coin, entering the quantity purchased, and specifying the purchase price. View, update, or delete assets from the portfolio. Analysis : Use pie charts and bar charts to analyze portfolio performance. Backtest trading strategies using historical data. Stay Updated : Access the latest news related to selected cryptocurrencies. Monitor live price charts and predictions. Dependencies The app relies on the following Python libraries:
streamlit: For building the web interface. pandas: For data manipulation and analysis. requests: For making API calls. plotly: For interactive visualizations. hashlib: For secure password hashing. sklearn: For machine learning-based price predictions. Install all dependencies using:

bash Copy 1 pip install streamlit pandas requests plotly scikit-learn APIs Used CoinGecko API : Fetches real-time cryptocurrency prices and historical data. Documentation: https://www.coingecko.com/en/api NewsAPI : Fetches the latest cryptocurrency-related news. Documentation: https://newsapi.org/ Customization

Navbar Includes social media icons (GitHub, LinkedIn, etc.) for branding. Twitter and Facebook icons have been removed as per the latest request.
Sidebar Enhanced with a visually appealing design, including a logo and motivational text. Added a checkbox for enabling/disabling email alerts.
Footer
Future Enhancements Email Notifications : Integrate a service like SendGrid to send real-time email alerts for portfolio updates. Advanced Analytics : Add more sophisticated trading strategies and machine learning models. Mobile Optimization : Ensure the app is fully responsive for mobile devices. Database Integration : Replace the users.csv file with a proper database (e.g., SQLite or PostgreSQL) for scalability. Contributors Quratulain Shah : Initial development and design. Your Name : Further enhancements and maintenance. License This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments Thanks to the developers of Streamlit , CoinGecko API , and NewsAPI for their excellent tools and services.