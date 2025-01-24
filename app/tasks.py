from celery import shared_task
from .meta_trader import fetch_one_minutes_mt5_data , fetch_last_year_mt5_data
from .detect import detect_flag_patterns
from redis_client import redis_client
from .models import init_db
from .db import get_db_connection
import pandas as pd
import re
from datetime import datetime , timedelta
# Initialize the database
init_db()

@shared_task
def fetch_data():
    """
    Fetch data from MetaTrader 5 and save it to Redis.
    """
    df = fetch_one_minutes_mt5_data()
    if df is not None:
        # Save raw data to Redis
        for index, row in df.iterrows():
            redis_client.hset("EURUSD:raw", index.isoformat(), row['close'])
        print("Data saved to Redis.")

@shared_task
def detect_and_save_patterns():
    """
    Detect flag patterns from redis data and save them to PostgreSQL.
    """
    # Fetch raw data from Redis
    raw_data = redis_client.hgetall("EURUSD:raw")
    if not raw_data:
        print("No data found in Redis.")
        return

    # Convert raw data to DataFrame
    timestamps = [key.decode('utf-8') for key in raw_data.keys()]

    # Extract numeric values from the byte strings
    prices = []
    for value in raw_data.values():
        # Decode the byte string to a regular string
        value_str = value.decode('utf-8')
        
        # Use a regular expression to extract the numeric value
        match = re.search(r'\d+\.\d+', value_str)  # Match a floating-point number
        if match:
            numeric_value = match.group(0)  # Extract the matched number
            prices.append(float(numeric_value))  # Convert to float

        else:
            raise ValueError(f"Could not extract numeric value from: {value_str}")

    # Create the DataFrame
    df = pd.DataFrame({"timestamp": timestamps, "close": prices})
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    # Detect flag patterns
    patterns = detect_flag_patterns(df)

    # Save detected patterns to PostgreSQL
    conn = get_db_connection()
    cursor = conn.cursor()
    for pattern in patterns:
        # Ensure the price is a clean float
        price = float(re.search(r'\d+\.\d+', str(pattern['price'])).group(0))
        print(f"Inserting pattern: timestamp={pattern['timestamp']}, price={price}, pattern={pattern['pattern']}")
        cursor.execute(
            "INSERT INTO flag_patterns (timestamp, price, pattern) VALUES (%s, %s, %s)",
            (pattern['timestamp'], str(pattern['price']), pattern['pattern'])
        )
    conn.commit()
    conn.close()
    print(f"Saved {len(patterns)} patterns to PostgreSQL.")


@shared_task
def cleanup_old_data():
    """
    Delete data older than 2 hours from Redis.
    """
    now = datetime.now()
    two_hours_ago = now - timedelta(hours=2)

    # Fetch all keys from Redis
    raw_data = redis_client.hgetall("EURUSD:raw")
    for key in raw_data.keys():
        timestamp = datetime.fromisoformat(key.decode('utf-8'))
        if timestamp < two_hours_ago:
            redis_client.hdel("EURUSD:raw", key)
    print("Deleted old data from Redis.")