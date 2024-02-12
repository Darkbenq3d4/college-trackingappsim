"""
    Esta parte representa el sensor del vehiculo
    conectado a SMS y enviando mensajes.
    La estructura del mensaje sera:
        Lat,lon,battSen,alt,vel,gradDir
"""

import paho.mqtt.client as paho
import time
import threading



"""
Setting Messages and host
"""
localtime = time.time()
localtimeFormated = time.localtime(localtime)
date = str(localtimeFormated.tm_year)+"-"+str(localtimeFormated.tm_mon)+"-"+str(localtimeFormated.tm_mday)+" "+str(localtimeFormated.tm_hour)+":"+str(localtimeFormated.tm_min)+":"+str(localtimeFormated.tm_sec)
receiverTopic = "Sistema/Receiver"
alertTopic = "Sistema/Alert"
msg = "45.252,-75.541,95,120,60,90, date: " + date
host = "localhost"

def on_connect(client, userdata, flags, rc):
     print("Conexion exitosa al sistema, esperando comando de activacion...")
     if not flags["session present"]:
          print("Conectando al sistema de alertas...")
          client.subscribe("Sistema/Alert")
          print("Conexion exitosa a Alertas")

def main():
        print("Espere...")
        while True:
            time.sleep(1)
            client.publish(topic=receiverTopic,payload=msg)
                

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
    else:
        print(msg.payload.decode("utf-8"))

if __name__ == '__main__':

    client =  paho.Client()
    client.on_connect = on_connect
    client.connect(host, 1883, 60)
    sub = threading.Thread(target=subscriber,name="Sub")
    pub = threading.Thread(target=main, name= "Pub")
    sub.start()
    pub.start()


    
    