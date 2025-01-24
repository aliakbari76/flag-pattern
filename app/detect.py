import pandas as pd

def detect_flag_patterns(df: pd.DataFrame, flagpole_threshold: float = 0.01, consolidation_threshold: float = 0.005) -> list:
    """
    Detect flag patterns in the price data.
    :param df: DataFrame with price data (columns: 'open', 'high', 'low', 'close')
    :param flagpole_threshold: Minimum percentage change for the flagpole
    :param consolidation_threshold: Maximum percentage change for the consolidation
    :return: List of dictionaries containing detected patterns with timestamp and price
    """
    patterns = []
    for i in range(1, len(df) - 5):  # Loop through the data
        # Calculate percentage change for the flagpole
        flagpole_change = (df['close'].iloc[i] - df['close'].iloc[i - 1]) / df['close'].iloc[i - 1]
        
        # Check for a strong flagpole movement
        if abs(flagpole_change) >= flagpole_threshold:
            # Look for consolidation in the next 5 candles
            consolidation = df['close'].iloc[i + 1:i + 6]
            consolidation_change = (consolidation.max() - consolidation.min()) / consolidation.min()
            
            # Check for low volatility consolidation
            if consolidation_change <= consolidation_threshold:
                # Check if the consolidation is in the opposite direction of the flagpole
                if (flagpole_change > 0 and consolidation.max() < df['close'].iloc[i]) or \
                   (flagpole_change < 0 and consolidation.min() > df['close'].iloc[i]):
                    patterns.append({
                        "timestamp": df.index[i],
                        "price": df['close'].iloc[i],
                        "pattern": "Flag"
                    })
                    print("found a new candidate!")
    
    return patterns