import MetaTrader5 as mt5
from datetime import datetime , timedelta
import pandas as pd

def fetch_last_year_mt5_data()-> pd.DataFrame | None:
    # connect to MetaTrader 5
    if not mt5.initialize(path = 'C:/Program Files/MetaTrader 5/terminal64.exe'):
        print("initialize() failed")
        mt5.shutdown()
        return None

    symbol = "EURUSD"
    timeframe = mt5.TIMEFRAME_H1  # 1-hour timeframe

    # Define the start and end time for the data
    end_time = datetime.now()
    start_time = end_time - timedelta(days=365)  # Last 365 days of data

    # Retrieve historical data
    rates = mt5.copy_rates_range(symbol, timeframe, start_time, end_time)

    # Shutdown MT5 connection
    mt5.shutdown()

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')  # Convert timestamp to datetime
    df.set_index('time', inplace=True)  # Set time as the index

    return df

def fetch_one_minutes_mt5_data()-> pd.DataFrame | None:
    # connect to MetaTrader 5
    if not mt5.initialize(path = 'C:/Program Files/MetaTrader 5/terminal64.exe'):
        print("initialize() failed")
        mt5.shutdown()
        return None

    symbol = "EURUSD"
    timeframe = mt5.TIMEFRAME_M1  # 1-MIN timeframe

    # Define the start and end time for the data
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=1)  # Last 1 min of data

    # Retrieve historical data
    rates = mt5.copy_rates_range(symbol, timeframe, start_time, end_time)

    # Shutdown MT5 connection
    mt5.shutdown()

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')  # Convert timestamp to datetime
    df.set_index('time', inplace=True)  # Set time as the index

    return df