from kafka import KafkaProducer,KafkaConsumer
from time import sleep
import re
#import os.path.basename
from random import choice

def publish_message(producer_instance, topic_name, value):
    try:
        #key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
        #sleep(0.05)
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9093','localhost:9094','localhost:9095'], api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

file_dict={}
file_obj_list=[]
in_files=open("files.txt",'r').readlines()
for i in in_files:
    print(i)
    file_dict[i.split("-")[1]]=connect_kafka_producer()
for j in in_files:
    print("./commentaries/" + j.strip())
    file_obj_list.append(open("./commentaries/" + j.strip(), 'r'))

file_dict

file_obj_list

while file_obj_list:
    file=choice(file_obj_list)
    line=file.readline()
    if line.strip() == "EOF":
        file_obj_list.remove(file)
        continue
    topic_name=file.name.split("-")[1]
    print(topic_name)
    publish_message(file_dict.get(topic_name),topic_name,line)
