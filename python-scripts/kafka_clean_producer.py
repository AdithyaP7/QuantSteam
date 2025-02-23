from kafka import KafkaProducer, KafkaConsumer
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

consumer = KafkaConsumer(
    "stock_data",
    bootstrap_servers=['localhost:9091'],
    group_id="producer2",
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

topic = 'cleaned_stock_data'


# need to fix this for realistic data. fit to some random values rn
initial_data = [
    {"open": 102.0, "high": 104.0, "low": 98.0, "close": 101.0, "volume": 1000000},
    {"open": 152.0, "high": 154.0, "low": 148.0, "close": 151.0, "volume": 1000000},
    {"open": 202.0, "high": 204.0, "low": 198.0, "close": 201.0, "volume": 1000000},
]

initial_values = [
    [d["open"], d["high"], d["low"], d["close"], d["volume"]] for d in initial_data
]

scaler = StandardScaler()
scaler.fit(initial_values)
for message in consumer:
    raw = message.value
    preprocessed = preprocess_data(raw, scaler)
    producer.send(topic, value=preprocessed)

    time.sleep(0.1)

# file_path = '../dummy/dummy_stock_data.csv'
# df = pd.read_csv(file_path)
# df = df.dropna()
# scaler = StandardScaler()
# scaler.fit(df[["open", "high", "low", "close", "volume"]])


# for index, row in df.iterrows():
#     raw_data = row.to_dict()
#     preprocessed_data = preprocess_data(raw_data, scaler)
#     producer.send(topic, value=preprocessed_data)
#     time.sleep(0.1)

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
consumer.close()


