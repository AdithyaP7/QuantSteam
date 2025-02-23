# QuantStream
A real-time stock market analytics system that leverages enhanced data streaming, processing, storage, and analytics to deliver a novel experience to everyday traders. 


Virtual Environment:  
python -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  


API Key:  
5SIOLTZC95CTPAJF

.env 
ALPHA_VANTAGE_API_KEY=5SIOLTZC95CTPAJF
SNOWFLAKE_USER=your_snowflake_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account_identifier

## Kafka
cd kafka_2.13-3.9.0  

(all in different terminals)

### Start Zookeeper Server
bin/zookeeper-server-start.sh config/zookeeper.properties  

### Start Kafka Server
bin/kafka-server-start.sh config/server.properties  

### Create Kafka Topic
bin/kafka-topics.sh --create --topic stock_data --bootstrap-server localhost:9091 --replication-factor 1 --partitions 1

### Start Consumer
bin/kafka-console-consumer.sh --topic stock_data --from-beginning --bootstrap-server localhost:9091

## Kafka Snowflake Sink Connector

Update the plugin.path in kafka connect-standalone properties.
(change for your specific path)
plugin.path=/Users/akshaymistry/Dev/gt/cs4440/QuantStream/kafka_2.13-3.9.0/libs





