import pandas as pd
import streamlit as st
from tvDatafeed import TvDatafeed, Interval
from pytz import timezone
import matplotlib.pyplot as plt
import numpy as np

# Title for Streamlit App
st.title('Stock Market Analyzer')

# Authentication details for TV Datafeed
username = #username
password = #password

# Creating TV Datafeed object
tv = TvDatafeed(username, password)

# Exchange selection
st.write("Select Exchange:")
exchange = st.selectbox('Exchange', ['BINANCE', 'NSE'])

# Symbols based on exchange
if exchange == 'NSE':
    symbols = [
        ' ', 'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'HINDUNILVR', 'KOTAKBANK', 'BHARTIARTL',
        'HCLTECH', 'HDFC', 'LT', 'AXISBANK', 'WIPRO', 'SBIN', 'ASIANPAINT', 'MARUTI', 'INDUSINDBK',
        'IOC', 'NTPC', 'POWERGRID', 'BAJFINANCE', 'TECHM', 'TITAN', 'ULTRACEMCO', 'ONGC', 'M&M',
        'COALINDIA', 'DRREDDY', 'SUNPHARMA', 'EICHERMOT', 'TATASTEEL', 'GRASIM', 'CIPLA', 'HEROMOTOCO',
        'JSWSTEEL', 'BPCL', 'UPL', 'SHREECEM', 'TATAMOTORS', 'NESTLEIND', 'GAIL', 'BRITANNIA', 'DIVISLAB',
        'HINDALCO', 'ADANIPORTS', 'HINDPETRO', 'HINDZINC', 'BAJAJ_AUTO', 'ITC', 'BAJAJFINSV',
        'BAJAJHLDNG', 'TATACONSUM', 'SBILIFE', 'HAVELLS', 'LICHSGFIN', 'AMBUJACEM', 'GODREJCP', 'PIDILITIND',
        'AUROPHARMA', 'HDFCLIFE', 'TORNTPHARM', 'MFSL', 'CADILAHC', 'MUTHOOTFIN', 'DABUR', 'BANDHANBNK',
        'HINDCOPPER', 'COLPAL', 'MINDTREE', 'GODREJIND', 'BANKBARODA', 'PNB', 'SIEMENS', 'IDEA', 'BHEL',
        'L&TFH', 'APOLLOHOSP', 'RBLBANK', 'BATAINDIA', 'JINDALSTEL', 'MRF', 'TVSMOTOR', 'PETRONET', 'BEL',
        'MGL', 'LUPIN', 'BALKRISIND', 'GLENMARK', 'NATIONALUM', 'GMRINFRA', 'MINDAIND', 'ICICIGI', 'TATACHEM',
        'BERGEPAINT', 'ESCORTS', 'UBL', 'IBULHSGFIN', 'RAMCOCEM', 'BOSCHLTD'
    ]
else:
    symbols = [
        ' ','BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 'SOLUSDT', 'DOGEUSDT', 'DOTUSDT', 'MATICUSDT',
       'AVAXUSDT', 'SHIBUSDT', 'LTCUSDT', 'TRXUSDT', 'UNIUSDT', 'LINKUSDT', 'BCHUSDT', 'ALGOUSDT', 'XLMUSDT',
    'ATOMUSDT', 'VETUSDT', 'FILUSDT', 'ICPUSDT', 'MANAUSDT', 'SANDUSDT', 'AXSUSDT', 'EGLDUSDT', 'AAVEUSDT',
    'KSMUSDT', 'MKRUSDT', 'YFIUSDT', 'SUSHIUSDT', 'COMPUSDT', 'CRVUSDT', 'SNXUSDT', 'RUNEUSDT', 'ZILUSDT',
    'ENJUSDT', 'CHZUSDT', 'HBARUSDT', 'GRTUSDT', 'FTTUSDT', 'LUNAUSDT', 'ONEUSDT', 'BTTUSDT', 'STMXUSDT',
    'ROSEUSDT', 'LRCUSDT', 'COTIUSDT', 'ZRXUSDT', 'BATUSDT', 'KAVAUSDT', 'RENUSDT', 'UMAUSDT', 'BALUSDT',
    'FETUSDT', 'CELRUSDT', 'DENTUSDT', 'HOTUSDT', 'CTKUSDT', 'STORJUSDT', 'ARUSDT', 'OCEANUSDT', 'AKROUSDT',
    'DGBUSDT', 'KMDUSDT', 'DOCKUSDT', 'LTOUSDT', 'RIFUSDT', 'WRXUSDT', 'STPTUSDT', 'HIVEUSDT', 'MDTUSDT',
    'PONDUSDT', 'DUSKUSDT', 'PERLUSDT', 'LOOMUSDT', 'CVCUSDT', 'MITHUSDT', 'COSUSDT', 'ARDRUSDT', 'VITEUSDT',
    'TROYUSDT', 'DGBUSDT', 'MBLUSDT', 'CTXCUSDT', 'MFTUSDT', 'DOCKUSDT', 'WTCUSDT', 'TWTUSDT', 'BEAMUSDT',
    'XEMUSDT', 'BTSUSDT', 'NAVUSDT', 'FTMUSDT', 'PHBUSDT', 'BANDUSDT', 'ERDUSDT', 'ANKRUSDT', 'LENDUSDT',
    'TCTUSDT'
    ]

# Symbol selection
selected_symbol = st.selectbox('Select Symbol', symbols)

# Fetching data for selected symbol
if exchange and selected_symbol:
    st.write(f"Fetching data for {selected_symbol} from {exchange}...")

    try:
        data = tv.get_hist(symbol=selected_symbol, exchange=exchange, interval=Interval.in_15_minute, n_bars=600)

        if data is None or data.empty:
            st.error(f"Failed to fetch data for {selected_symbol}. Please check your exchange and symbol.")
        else:
            # Reset index if necessary
            if data.index.name == 'datetime' or data.index.name is not None:
                data.reset_index(inplace=True)

            # Convert 'datetime' to timezone-aware datetime and localize to IST
            data['datetime'] = pd.to_datetime(data['datetime'])

            data.set_index('datetime', inplace=True)
            st.write(data.iloc[::-1])

            # Calculate EMA 20, 50, and 200
            data['EMA_20'] = data['close'].ewm(span=20, adjust=False).mean()
            data['EMA_50'] = data['close'].ewm(span=50, adjust=False).mean()
            data['EMA_200'] = data['close'].ewm(span=200, adjust=False).mean()

            # Plot Close Price and EMA 20, 50, 200
            fig, ax = plt.subplots(figsize=(14, 8))
            ax.plot(data['close'], label='Close Price', color='blue', linewidth=2)
            ax.plot(data['EMA_20'], label='20-period EMA', color='red', linestyle='-.')
            ax.plot(data['EMA_50'], label='50-period EMA', color='green', linestyle='-.')
            ax.plot(data['EMA_200'], label='200-period EMA', color='purple', linestyle='-.')
            ax.set_title(f'{selected_symbol} Exponential Moving Average (EMA)', fontsize=16)
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Price (USD)' if exchange == 'BINANCE' else 'Price (INR)', fontsize=12)
            ax.legend(loc='upper left')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Display plot
            st.pyplot(fig)

            # RSI Calculation
            def calculate_rsi(data, window=14):
                delta = data['close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
                rs = gain / loss
                return 100 - (100 / (1 + rs))

            data['RSI'] = calculate_rsi(data)

            # Plot RSI
            plt.figure(figsize=(16, 8))
            plt.plot(data['RSI'], label='RSI', color='orange', linewidth=1)
            plt.axhline(70, color='r', linestyle='--', alpha=0.7)
            plt.axhline(30, color='g', linestyle='--', alpha=0.7)
            plt.title(f'{selected_symbol} Relative Strength Index (RSI)', fontsize=14)
            plt.xlabel('Date')
            plt.ylabel('RSI')
            plt.legend()
            plt.grid(True, alpha=0.3)

            st.pyplot(plt)

            # Strong Buy / Strong Sell Indicator based on SMA
            data['SMA_20'] = data['close'].rolling(window=20).mean()
            data['Strong_Buy'] = np.where(data['close'] > data['SMA_20'], 1, 0)
            data['Strong_Sell'] = np.where(data['close'] < data['SMA_20'], -1, 0)

            # Plotting Strong Buy / Sell indicators
            plt.figure(figsize=(16, 8))
            plt.plot(data['close'], label='Close Price', color='blue', linewidth=2)
            plt.scatter(data.index[data['Strong_Buy'] == 1], data['close'][data['Strong_Buy'] == 1], marker='^', color='g', label='Strong Buy')
            plt.scatter(data.index[data['Strong_Sell'] == -1], data['close'][data['Strong_Sell'] == -1], marker='v', color='r', label='Strong Sell')
            plt.title(f'{selected_symbol} Strong Buy / Strong Sell Indicators', fontsize=14)
            plt.xlabel('Date')
            plt.ylabel('Price (USD)' if exchange == 'BINANCE' else 'Price (INR)')
            plt.legend()
            plt.grid(True, alpha=0.3)

            st.pyplot(plt)

            # Add toggle button to show/hide the additional graph
            if st.button('Advanced Analysis'):
                # Bollinger Bands and Fibonacci levels
                data['Bollinger_Mid'] = data['close'].rolling(window=20).mean()
                data['Bollinger_Upper'] = data['Bollinger_Mid'] + 2 * data['close'].rolling(window=20).std()
                data['Bollinger_Lower'] = data['Bollinger_Mid'] - 2 * data['close'].rolling(window=20).std()

                # Fibonacci Levels
                high = data['close'].max()
                low = data['close'].min()
                diff = high - low
                data['Fib_23.6'] = high - 0.236 * diff
                data['Fib_38.2'] = high - 0.382 * diff
                data['Fib_50.0'] = high - 0.5 * diff
                data['Fib_61.8'] = high - 0.618 * diff

                # Plot Advanced Analysis
                fig, ax1 = plt.subplots(figsize=(14, 8))

                ax1.plot(data['close'], label='Close Price', color='blue', linewidth=2)
                ax1.plot(data['EMA_50'], label='50-period EMA', color='green', linestyle='-.')
                ax1.plot(data['EMA_200'], label='200-period EMA', color='purple', linestyle='-.')
                ax1.plot(data['Bollinger_Upper'], label='Bollinger Upper Band', color='brown', linestyle='-.', alpha=0.3)
                ax1.plot(data['Bollinger_Lower'], label='Bollinger Lower Band', color='brown', linestyle='-.', alpha=0.3)

                ax1.axhline(data['Fib_23.6'].iloc[-1], color='cyan', linestyle='--', label='Fib 23.6%')
                ax1.axhline(data['Fib_38.2'].iloc[-1], color='yellow', linestyle='--', label='Fib 38.2%')
                ax1.axhline(data['Fib_50.0'].iloc[-1], color='magenta', linestyle='--', label='Fib 50.0%')
                ax1.axhline(data['Fib_61.8'].iloc[-1], color='blue', linestyle='--', label='Fib 61.8%')

                ax1.set_title(f'{selected_symbol} Advanced Technical Indicators', fontsize=16)
                ax1.set_xlabel('Date', fontsize=12)
                ax1.set_ylabel('Price (USD)' if exchange == 'BINANCE' else 'Price (INR)', fontsize=12)
                ax1.legend(loc='upper left')

                plt.xticks(rotation=45)
                plt.tight_layout()

                st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
else:
    st.info("Please select both exchange and symbol to proceed.")
