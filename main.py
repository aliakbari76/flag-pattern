from app.models import init_db
from redis_client import redis_client
from app.app import fetch_data , detect_and_save_patterns , clean_data_from_redis
import re
def initialize_application():
    """
    Initialize the application by setting up the database and testing connections and detecting flag pattern on 1H timeframe in last year.
    """
    # Initialize the database
    init_db()
    print("Database initialized.")

    # Test Redis connection
    try:
        redis_client.ping()
        print("Redis connection successful.")
    except Exception as e:
        print(f"Redis connection failed: {e}")
    # get data for one last year in 1h timeframe and detect falg pattern on it!
    
    fetch_data()
    detect_and_save_patterns()
    clean_data_from_redis()


def main():
    initialize_application()

if __name__ == "__main__":
    main()