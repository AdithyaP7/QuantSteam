from kafka import KafkaProducer
import json
import pandas as pd
from sklearn.preprocessing import StandardScaler
from datetime import datetime

# Preprocessing function
def preprocess_data(data, scaler):
    # Convert string fields to the correct types (e.g., float for numeric values)
    data["open"] = float(data["open"])
    data["high"] = float(data["high"])
    data["low"] = float(data["low"])
    data["close"] = float(data["close"])
    data["volume"] = int(data["volume"])

    # Apply normalization (standardization)
    scaled_data = scaler.transform([[data["open"], data["high"], data["low"], data["close"], data["volume"]]])

    # Add new columns with normalized values
    data["normalized_open"] = round(scaled_data[0][0], 2)
    data["normalized_high"] = round(scaled_data[0][1], 2)
    data["normalized_low"] = round(scaled_data[0][2], 2)
    data["normalized_close"] = round(scaled_data[0][3], 2)
    data["normalized_volume"] = round(scaled_data[0][4], 2)

    # Example of adding calculated fields (e.g., moving average)
    data["moving_average"] = round((data["open"] + data["high"] + data["low"] + data["close"]) / 4, 2)

    # Example of calculating RSI (Relative Strength Index) - placeholder calculation
    data["rsi"] = 70  # Normally you'd compute RSI here, this is a placeholder

    return data

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers=['localhost:9091'],  # Adjust to your Kafka setup
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize JSON data
)

# Kafka topic to send preprocessed data
topic = 'cleaned_stock_data'

# Read the dummy data CSV file into a DataFrame
file_path = '../dummy/dummy_stock_data.csv'
df = pd.read_csv(file_path)

# Drop rows with missing values
df = df.dropna()

# Initialize the StandardScaler
scaler = StandardScaler()

# Fit the scaler on the numerical columns for normalization
scaler.fit(df[["open", "high", "low", "close", "volume"]])

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Convert the row to a dictionary
    raw_data = row.to_dict()

    # Preprocess the raw data
    preprocessed_data = preprocess_data(raw_data, scaler)

    # Send preprocessed data to Kafka topic
    producer.send(topic, value=preprocessed_data)

    # Optionally, add a small delay to avoid flooding Kafka too quickly
    # time.sleep(0.1)

# Wait for any outstanding messages to be delivered and delivery reports to be received
producer.flush()

print(f"Data sent to topic '{topic}'.")

# # Before cleaning
# print("Missing values before cleaning:")
# print(df.isna().sum())

# # After cleaning
# df_cleaned = preprocess_data(df, scaler)  # Assuming this is the method to preprocess
# print("Missing values after cleaning:")
# print(df_cleaned.isna().sum())

# Close the producer after use
producer.close()


