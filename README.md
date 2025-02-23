# QuantStream
A real-time stock market analytics system that leverages enhanced data streaming, processing, storage, and analytics to deliver a novel experience to everyday traders. 


Virtual Environment:  
python -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  


API Key:  
5SIOLTZC95CTPAJF

## Kafka
cd kafka_2.13-3.9.0  

(all in different terminals)

### Start Zookeeper Server
bin/zookeeper-server-start.sh config/zookeeper.properties  

### Start Kafka Server
bin/kafka-server-start.sh config/server.properties  

### Create Kafka Topic
bin/kafka-topics.sh --create --topic my_topic123 --bootstrap-server localhost:9091 --replication-factor 1 --partitions 1

### Start Consumer
bin/kafka-console-consumer.sh --topic my_topic123 --from-beginning --bootstrap-server localhost:9091

