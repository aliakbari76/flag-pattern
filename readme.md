# Flag Pattern Detector

This project detects flag patterns in EUR/USD price data using MetaTrader 5, Redis, PostgreSQL, and Celery. It fetches data from MetaTrader 5, stores it in Redis, detects flag patterns, and saves the results to PostgreSQL.

## Prerequisites

Before running the project, ensure the following are installed and running on your machine:

### MetaTrader 5:
- Install MetaTrader 5 from the official website.
- Ensure the terminal is running and logged in to your account.

### PostgreSQL:
- Install PostgreSQL from the official website.
- Create a database named `flag_patterns` and a user with the necessary permissions.

### Redis:
- Install Redis from the official website.
- Ensure the Redis server is running on `localhost:6379`.

### Python:
- Install Python 3.9 or later from the official website.

## Setup

### 1. Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/flag-pattern-detector.git
cd flag-pattern-detector
```

### 2. Install Dependencies
Run the `install_app.bat` file to install the required Python dependencies:

```bash
install_app.bat
```

This script runs the following command:

```bash
pip install -r requirements.txt
```

### 3. Configure the Project

#### MetaTrader 5:
Update the path in `meta_trader.py` to point to your MetaTrader 5 installation.

#### PostgreSQL:
Update the connection details in `db.py`:

```python
def get_db_connection():
    return psycopg2.connect(
        dbname="flag_patterns",
        user="postgres",
        password="yourpassword",
        host="localhost",
        port="5432",
    )
```

#### Redis:
Ensure Redis is running on `localhost:6379`. If not, update the connection details in `redis_client.py`.

### 4. Run the Project
Run the `run_app.bat` file to start the project:

```bash
run_app.bat
```

This script runs the following commands:

```bash
celery -A celery_config worker --loglevel=info -P solo
celery -A celery_config beat --loglevel=info
```

## Project Structure

```plaintext
flag-pattern-detector/
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── detect.py
│   ├── meta_trader.py
│   ├── models.py
│   ├── tasks.py
├── celery_config.py
├── main.py
├── redis_client.py
├── requirements.txt
├── install_app.bat
├── run_app.bat
├── README.md
```

## How It Works

### Data Fetching:
The `fetch_data` task fetches EUR/USD price data from MetaTrader 5 every 1 minute and saves it to Redis.

### Pattern Detection:
The `detect_and_save_patterns` task checks for flag patterns every 5 minutes and saves the results to PostgreSQL.

### Data Cleanup:
The `cleanup_old_data` task deletes data older than 2 hours from Redis.

## Commands

### Install Dependencies
```bash
install_app.bat
```

### Run the Project
```bash
run_app.bat
```

### Stop the Project
Press `Ctrl + C` in the terminal to stop the Celery worker and beat.

## Troubleshooting

### MetaTrader 5 Connection Issues:
- Ensure MetaTrader 5 is running and logged in.
- Verify the path in `meta_trader.py` is correct.

### PostgreSQL Connection Issues:
- Ensure PostgreSQL is running and the database `flag_patterns` exists.
- Verify the connection details in `db.py`.

### Redis Connection Issues:
- Ensure Redis is running on `localhost:6379`.
- Verify the connection details in `redis_client.py`.

### Celery Worker Issues:
- Ensure the `include` parameter in `celery_config.py` points to the correct module (`app.tasks`).

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or feedback, feel free to reach out:

- **Name**: ali akbari
- **Email**: ali.akbari.76.amol@gmail.com
- **GitHub**: [aliakbari76](https://github.com/aliakbari76)

