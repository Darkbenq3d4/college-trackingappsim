"""
    Esta parte representa el sensor del vehiculo
    conectado a SMS y enviando mensajes.
    La estructura del mensaje sera:
        Lat,lon,battSen,alt,vel,gradDir
"""

import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import time as Ti

"""
Setting Messages and host
"""
localtime = Ti.time()
localtimeFormated = Ti.localtime(localtime)
date = str(localtimeFormated.tm_year)+"-"+str(localtimeFormated.tm_mon)+"-"+str(localtimeFormated.tm_mday)+" "+str(localtimeFormated.tm_hour)+":"+str(localtimeFormated.tm_min)+":"+str(localtimeFormated.tm_sec)
receiverTopic = "Sistema/Receiver"
alertTopic = "Sistema/Alert"


msgs = [{'topic': receiverTopic, 'payload':"45.252,-75.541,95,120,60,90, date: " + date},
        {'topic': receiverTopic, 'payload':"45.252,-73.343,85,110,60,90, date: " + date},
        {'topic': receiverTopic, 'payload':"45.252,-77.233,65,110,60,90, date: " + date},
        {'topic': receiverTopic, 'payload':"45.252,-65.543,53,109,60,90, date: " + date}]

host = "localhost"

def on_message(client, obj, msg):
    if msg.payload.decode("utf-8") == "1" and msg.topic == alertTopic:
        print ("Boton de Alerta Activado - ",date,sep = " ")
        print ("A la espera de mensajes...")
        publish.multiple(msgs, hostname = host)
    elif msg.topic == alertTopic and msg.payload.decode("utf-8") == "2":
        print ("Alerta desactivada, sensor pasa a standby")
    else:
        print(msg.payload.decode("utf-8"))



def on_connect(client, userdata, flags, rc):
     print("Conexion exitosa al sistema, esperando comando de activacion...")
     print("Conectado a... '"+str(flags)+"', '"+str(rc)+"'")
     if not flags["session present"]:
          print("Conectando al sistema de alertas...")
          client.subscribe("Sistema/#")
          print("Conexion exitosa a Alertas")

if __name__ == '__main__':

    client =  paho.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, 1883, 60)
    client.loop_forever()



    
    