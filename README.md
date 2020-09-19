# Handling-Multiple-Data-Streams-and-Processing-in-Real-Time
Objective is to generate real-time scorecards of ICC world cup matches from live commentary.
Implemented a system to  generate real-time scorecard of all matches simultaneously by receiving simulated live commentary from Kafka server

--------------------------------------------------------------------------------------------------------------------------------------------

Maintain the Directory Structure as followes:

194161003
  - commentaries
    * 194161003-4143-commentary.txt
			.  
			.  
			.  

    * 194161003-4192-commentary.txt  
  - scorecards  
  - main.py  
  - Producer.py  
  - Consumer.py  
  - Genarate_Scorecard.py   
  - teams.txt  
  
--------------------------------------------------------------------------------------------------------------------------------------------

This setup is build with 3 zookeeper Severs and 3 kafka brokers (server/node)

steps to run program:

1. configure system with 3 zookeeper servers having client port (localhost:2183,localhost:2184,localhost:2185)
and 3 Kafka Brokers (localhost:9092,localhost:9093,localhost:9094)
 
2. Start all servers

3. run 194161003_q2.py

4. check all matches scorecards in scorecard folder

sleep timer can be introduced in producer and consumer for real match simulation (both timer should be set accordingly)

