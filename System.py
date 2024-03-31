"""
    Esta parte representa el sensor del vehiculo
    conectado a SMS y enviando mensajes.
    La estructura del mensaje sera:
        Lat,lon,battSen,alt,vel,gradDir,date
"""

import paho.mqtt.client as paho
import time
import threading
import random
import pymongo
import json

"""
Setting Messages and host
"""
localtime = time.time()
localtimeFormated = time.localtime(localtime)
date = str(localtimeFormated.tm_year)+"-"+str(localtimeFormated.tm_mon)+"-"+str(localtimeFormated.tm_mday)+" "+str(localtimeFormated.tm_hour)+":"+str(localtimeFormated.tm_min)+":"+str(localtimeFormated.tm_sec)
receiverTopic = "Sistema/Receiver"
alertTopic = "Sistema/Alert"
historyTopic = "Sistema/Historial"
msgs = ["155215512354,41.252,-75.541,95,120,65,90," + date,
        "155215512354,44.252,-73.541,95,120,60,30,: " + date,
        "155215512354,43.252,-72.541,95,120,40,40,: " + date,
        "155215512354,42.252,-71.541,95,120,70,20,: " + date,
        "155215512354,41.222,-75.541,95,120,60,60,: " + date,
        "155215512354,45.242,-76.541,95,120,50,70,: " + date,]
host = "localhost"

def on_connect(client:paho.Client, userdata, flags, rc):
     print("Conexion exitosa al sistema, esperando comando de activacion...")
     if not flags["session present"]:
          print("Conectando al sistema de alertas...")
          client.subscribe([(alertTopic,1),(historyTopic,1)])
          print("Conexion exitosa a Alertas")

def main():
        print("Espere...")
        while True:
            time.sleep(1)
            client.publish(topic=receiverTopic,payload=msgs[random.randrange(start=0,stop=5)])
                
def insertImeiHistoryData(message:str):
     #message_format "imeinumber,lat,lon,battSen,alt,vel,gradDir,date"
      msgFormat = message.split(sep=",")
      newDoc = {
           "imei":msgFormat[0],
           "lat":msgFormat[1],
           "lon":msgFormat[2],
           "battery_sensor":msgFormat[3],
           "altitude":msgFormat[4],
           "speed": msgFormat[5],
           "direction_degree": msgFormat[6],
           "date": msgFormat[7]
           }
      collection.insert_one(document=newDoc)
     
def getImeiHistoryData(imei:str):
     unit_history = collection.find({"imei":imei})
     for doc in unit_history:
          print("Fecha: "+doc["date"]+
                ", Coordenadas: "+doc["lat"]+", "+doc["lon"]+
                ", Altitud: "+doc["altitude"]+
                ", IMEI: "+doc["imei"]+
                ", Velocidad: "+doc["speed"])

def subscriber():
     client.on_message = on_message
     client.loop_forever()

def on_message(client: paho.Client , obj, msg):
    if msg.payload.decode("utf-8") == "1" and msg.topic == alertTopic:
        print ("Boton de Alerta Activado - ",date,sep = " ")
        print ("A la espera de mensajes...")
        client.subscribe(receiverTopic)
    elif msg.topic == alertTopic and msg.payload.decode("utf-8") == "2":
        print ("Alerta desactivada, sensor pasa a standby")
        client.unsubscribe(receiverTopic)       
    elif msg.topic == historyTopic:
         Imei = msg.payload.decode("utf-8")
         print("Historial de la unidad IMEI: "+Imei)
         getImeiHistoryData(imei=Imei)
    elif msg.topic == receiverTopic:
        print(msg.payload.decode("utf-8"))
        insertImeiHistoryData(msg.payload.decode("utf-8"))

if __name__ == '__main__':

    MonClient = pymongo.MongoClient("mongodb://localhost:27017") #Creando conexion local
    db = MonClient["track_project_db"]
    collection = db["imei_history"]
    client =  paho.Client()
    client.on_connect = on_connect
    client.connect(host, 1883, 60)
    sub = threading.Thread(target=subscriber,name="Sub")
    pub = threading.Thread(target=main, name= "Pub")
    sub.start()
    pub.start()