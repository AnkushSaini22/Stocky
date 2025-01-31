# Stocky

## Introduction
The **Stock Market Analyzer** is a comprehensive web application built using **Streamlit** and **TV Datafeed** for fetching real-time stock and cryptocurrency data. The app allows users to analyze the stock market with various technical indicators, including **Exponential Moving Averages (EMA)**, **Relative Strength Index (RSI)**, **Simple Moving Average (SMA)**, **Bollinger Bands**, and **Fibonacci Retracements**. The data is sourced from exchanges like **Binance** and **NSE**, and users can select the symbol and exchange for analysis.

## Problem Statement
As an investor or trader, analyzing stock market data is crucial for making informed decisions. However, manual analysis can be time-consuming and requires a deep understanding of various technical indicators. This project aims to automate the process of fetching real-time data and visualizing technical indicators, making it easier for traders to track the market.

## Key Features
1. **Stock Data Fetching**: Retrieve data from **Binance** and **NSE** exchanges.
2. **Exponential Moving Averages (EMA)**: Display 20, 50, and 200-period EMAs on the stock price.
3. **Relative Strength Index (RSI)**: Calculate and plot RSI to identify overbought or oversold conditions.
4. **Strong Buy / Strong Sell Indicator**: Mark "Strong Buy" or "Strong Sell" signals based on Simple Moving Average (SMA).
5. **Advanced Analysis**: Option to display additional indicators like **Bollinger Bands** and **Fibonacci Levels**.
6. **Interactive Interface**: Interactive selection of exchange, stock symbol, and data visualizations using **Streamlit**.

## Installation

### Requirements
To run the application, ensure you have the following Python libraries installed:

```bash
pip install pandas streamlit tvDatafeed matplotlib numpy pytz
```

### Running the App
1. Clone the repository.
2. Ensure you have the necessary credentials for **TV Datafeed** (username and password).
3. Run the app using Streamlit:

```bash
streamlit run app.py
```

## How the Solution Works

### Data Fetching
- The user selects the exchange (**BINANCE** or **NSE**) and stock symbol.
- The app fetches the data using the **TV Datafeed API** with the selected parameters.
- The fetched data includes stock prices, which are displayed in a table.

### Technical Indicators
- **Exponential Moving Averages (EMA)**: The app calculates the **EMA for 20, 50, and 200 periods**, which are then plotted on the stock price chart.
- **Relative Strength Index (RSI)**: The RSI is calculated to determine overbought or oversold conditions, with 70 indicating overbought and 30 indicating oversold. These thresholds are plotted as horizontal lines.
- **Strong Buy / Strong Sell Indicator**: Based on the 20-period SMA, the app marks points where the price is above (strong buy) or below (strong sell) the SMA.

### Advanced Indicators (Optional)
The user can toggle additional technical analysis like **Bollinger Bands** and **Fibonacci Levels**:
- **Bollinger Bands**: Displays upper and lower bands based on the 20-period moving average and standard deviation.
- **Fibonacci Levels**: Automatically calculates key Fibonacci retracement levels and plots them on the chart.

### Visualization
- The app uses **Matplotlib** for visualizing stock prices, indicators, and buy/sell signals.
- It provides an interactive chart with various technical analysis tools that can be customized by the user.

## Usage

### Step 1: Select Exchange
- Choose between **Binance** and **NSE** to fetch the data.

### Step 2: Select Symbol
- Pick a stock or cryptocurrency symbol for analysis.

### Step 3: View Data and Indicators
- The stock/crypto data is fetched and displayed.
- **EMA**, **RSI**, and **Strong Buy/Sell indicators** are plotted on the chart.
- Optionally, the user can toggle to see **Bollinger Bands** and **Fibonacci Retracements**.

### Step 4: Analyze
- Use the charts and indicators to analyze market trends, identify buying or selling opportunities, and predict future movements.

## Code Walkthrough

### Data Fetching and Processing
```python
data = tv.get_hist(symbol=selected_symbol, exchange=exchange, interval=Interval.in_15_minute, n_bars=600)
```
- This fetches the historical price data for the selected symbol and exchange.
- The data is processed to calculate the EMAs and RSI.

### Calculating Indicators
- **EMA**:
```python
data['EMA_20'] = data['close'].ewm(span=20, adjust=False).mean()
data['EMA_50'] = data['close'].ewm(span=50, adjust=False).mean()
data['EMA_200'] = data['close'].ewm(span=200, adjust=False).mean()
```
- **RSI**:
```python
data['RSI'] = calculate_rsi(data)
```
- **Strong Buy / Strong Sell**:
```python
data['Strong_Buy'] = np.where(data['close'] > data['SMA_20'], 1, 0)
data['Strong_Sell'] = np.where(data['close'] < data['SMA_20'], -1, 0)
```

### Plotting
- The app uses **Matplotlib** to generate charts:
```python
fig, ax = plt.subplots(figsize=(14, 8))
ax.plot(data['close'], label='Close Price', color='blue', linewidth=2)
ax.plot(data['EMA_20'], label='20-period EMA', color='red', linestyle='-.')
ax.plot(data['EMA_50'], label='50-period EMA', color='green', linestyle='-.')
ax.plot(data['EMA_200'], label='200-period EMA', color='purple', linestyle='-.')
```

## Conclusion
This **Stock Market Analyzer** provides a user-friendly interface for analyzing stocks and cryptocurrencies with advanced technical indicators. It’s a powerful tool for traders to help make data-driven decisions using real-time market data and visualizations.

---
