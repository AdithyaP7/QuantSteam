from kafka import KafkaProducer
import json
import time
import pandas as pd
from sklearn.preprocessing import StandardScaler
from datetime import datetime

def preprocess_data(data, scaler):

    data["open"] = float(data["open"])
    data["high"] = float(data["high"])
    data["low"] = float(data["low"])
    data["close"] = float(data["close"])
    data["volume"] = int(data["volume"])

    #normalize
    scaled_data = scaler.transform([[data["open"], data["high"], data["low"], data["close"], data["volume"]]])

    data["normalized_open"] = round(scaled_data[0][0], 2)
    data["normalized_high"] = round(scaled_data[0][1], 2)
    data["normalized_low"] = round(scaled_data[0][2], 2)
    data["normalized_close"] = round(scaled_data[0][3], 2)
    data["normalized_volume"] = round(scaled_data[0][4], 2)

    data["moving_average"] = round((data["open"] + data["high"] + data["low"] + data["close"]) / 4, 2)

    data["rsi"] = 70

    return data

producer = KafkaProducer(
    bootstrap_servers=['localhost:9091'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'cleaned_stock_data'

file_path = '../dummy/dummy_stock_data.csv'
df = pd.read_csv(file_path)
df = df.dropna()
scaler = StandardScaler()
scaler.fit(df[["open", "high", "low", "close", "volume"]])


for index, row in df.iterrows():
    raw_data = row.to_dict()
    preprocessed_data = preprocess_data(raw_data, scaler)
    producer.send(topic, value=preprocessed_data)
    time.sleep(0.1)
    
producer.flush()

print(f"Data sent to topic '{topic}'.")

# # Before cleaning
# print("Missing values before cleaning:")
# print(df.isna().sum())

# # After cleaning
# df_cleaned = preprocess_data(df, scaler)  # Assuming this is the method to preprocess
# print("Missing values after cleaning:")
# print(df_cleaned.isna().sum())

producer.close()


