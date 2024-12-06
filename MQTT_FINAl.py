import network
import time
from math import sin
from umqtt.simple import MQTTClient
from machine import I2C, Pin
from bmp280 import *

#PIN INITIATION

sda = Pin(16, Pin.PULL_UP)
scl = Pin(17, Pin.PULL_UP)

#I2C INITIATION

bus=I2C(0,sda=sda, scl=scl, freq=300000)
print("I2C Address      : "+hex(bus.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(bus))

#SENSOR DATA GATHERDING

bme = BMP280(bus)
temp = round(bme.temperature )   
atm= round(bme.pressure/101300)


# NET INFO
wifi_ssid = "TP-Link_7504"
wifi_password = "83922800"

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

#MQTT LOGIN INFO

mqttServer   = "mqtt3.thingspeak.com"
mqttClientID = "GxUqES8cMxQ9CBY0LDsnBzs"  
mqttUser     = "GxUqES8cMxQ9CBY0LDsnBzs"  
mqttPass     = "I9KOfiLBLC/Y8lRY2vE37W7J"
mqttTopic    = "channels/2770859/publish"

#MQTT CLIENT INITIATION
cliente = MQTTClient (mqttClientID, mqttServer, port=1883, user=mqttUser, password=mqttPass)
#MQTT CLIENT CONECTION  
cliente.connect ()
   
#DATA PUBLISHING
while (True):
        time.sleep (60)
        
        print ("T={:02d} ºC, ATM={:02d} %".format (temp,atm))
        
        datos = "field1="+str(temp)+"&field2="+str(atm)
        
        cliente.publish(topic=mqttTopic, msg=datos) 
               
 
else:
       print ("Not connected")
       miRed.active (False)
       mqtt_client.disconnect()