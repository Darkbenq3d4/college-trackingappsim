# Tracking App Simulator using Mosquitto
College assigment for a Real System Aplication in the makings... 
David Rosario 22-0904

## Dependencies used
* Mqtt - Paho
* Mosquitto and Mosquitto_client
Both dependencies are in file dependencies.sh

## Problems solved using Concurrence
* Used threading to maintain a number of clients active and running without colissioning between them on the process time. ( In this case, I'm using one client that goes in a forever loop catching messages).
  
