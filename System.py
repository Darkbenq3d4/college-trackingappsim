"""
    Esta parte representa el sensor del vehiculo
    conectado a SMS y enviando mensajes.
    La estructura del mensaje sera:
        Lat,lon,battSen,alt,vel,gradDir
"""

import paho.mqtt.client as paho
import time as Ti

"""
Setting Messages and host
"""
localtime = Ti.time()
localtimeFormated = Ti.localtime(localtime)
date = str(localtimeFormated.tm_year)+"-"+str(localtimeFormated.tm_mon)+"-"+str(localtimeFormated.tm_mday)+" "+str(localtimeFormated.tm_hour)+":"+str(localtimeFormated.tm_min)+":"+str(localtimeFormated.tm_sec)
receiverTopic = "Sistema/Receiver"
alertTopic = "Sistema/Alert"


msgs = "45.252,-75.563,95,120,60,90," + date

host = "localhost"

def on_message(client, obj, msg):
    print ("Datos recibidos",date,msg.payload.decode("utf-8"),sep = " ")
    if msg.payload.decode("utf-8") == "1":
        client.publish(receiverTopic, msgs)



def on_connect(client, userdata, flags, rc):
     print("Conexion exitosa al sistema, esperando comando de activacion...")
     print("Conectado a... '"+str(flags)+"', '"+str(rc)+"'")
     if not flags["session present"]:
          print("Conectando al sistema de alertas...")
          client.subscribe("Sistema/#")
          print("Conexion exitosa a Alertas")

# def on_connectPub(client, userdata, flags, rc):
#      print("Conexion exitosa al recibidor, esperando comando de activacion...")
#      print("Conectado a... '"+str(flags)+"', '"+str(rc)+"'")
#      if not flags["session present"]:
#           print("Conectando al recibidor...")
#           client.subscribe(receiverTopic)
#           print("Conexion exitosa al recibidor")
             
      
if __name__ == '__main__':

    client =  paho.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, 1883, 60)
    client.loop_forever()



    
    