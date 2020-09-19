from kafka import KafkaProducer,KafkaConsumer
from time import sleep
import Genarate_Scorecard
import random
import re
from random import randint

def create_consumer(topic_name):
    consumer = KafkaConsumer(topic_name, auto_offset_reset='earliest',
                             bootstrap_servers=['localhost:9093','localhost:9094','localhost:9095'],enable_auto_commit=True,
                             group_id="commentators",api_version=(0, 10), consumer_timeout_ms=500,
                             max_poll_records=50,max_poll_interval_ms=50000)
    #print(topic_name)
    return consumer

class Test_Consumer:
    def __init__(self,file_name):
        self.file_name=file_name
        #self.line
    def write_to_file(self,line):
        fout=open(self.file_name,"a+")
        fout.write(line)
        fout.write("\n")
        fout.close()


def consume_data(consumer,obj):
    """consumer = KafkaConsumer(topic_name,auto_offset_reset='earliest',
                             bootstrap_servers=['localhost:9092'],
                             api_version=(0, 10), consumer_timeout_ms=500)
    """
    count=0
    #print(topic_name)
    #file_name=str(consumer.topics())+".txt"
    try:
        for msg in consumer:
            #print(msg.value)
            value=msg.value.decode('utf-8')

            #print(value)
            #if not re.search(topic_name,value):
            #print(len(msg))

            count+=1
            print((value.strip()))
            obj.redirect(value.strip())

        consumer.commit()
    #sleep(0.01)
    except Exception as ex:
        pass
    finally:
        return count
    #print(len(msg))


#consume_data_2("new")

file_dict={}
file_obj_out_list=[]
in_files=open("files.txt").readlines()
random.shuffle(in_files)
#print(in_files)
for i in in_files:
    match_id=i.split("-")[1]
    file_dict[match_id]=[create_consumer(match_id),
                                Genarate_Scorecard.match("./scorecards/" + "194161003-"+match_id+"-scorecard-computed.txt")]


count = 1
while count:

    count=0
   # c7.topics()
    for k,v in file_dict.items():

        count+=consume_data(v[0],v[1])

