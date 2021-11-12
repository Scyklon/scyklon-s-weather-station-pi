"""
'pluviometro'
==================================
Pluviometro de balança simples.
Envia as informaçoes na dashboard
adafruit.io e salva as informaçoes
na db influx.

Autor: G.Goulart
"""
# Importa os modulos python
import urllib.request
import board
import digitalio
import bmpsensor
import time
import sys
import datetime
from gpiozero import Button
from Adafruit_IO import Client, Feed, RequestError
from influxdb import InfluxDBClient

# Configura as variaveis da conexao a InfluxDB 
host = "localhost" # Seu ip
port = 8086 # porta padrao
user = "" # usuario do influx
password = "" # senha influx
dbname = "weather-station" # nome da database


# Cria o objeto cliente InfluxDB
client = InfluxDBClient(host, port, user, password, dbname)

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'your adafruit io key'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'your adafruit io user'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# think of measurement as a SQL table, it's not...but...
measurement = "station"
# location will be used as a grouping tag later
location = "sede"

try: # if we have a 'digital' feed
    rain = aio.feeds('rain')
    bmptemp = aio.feeds('bmptemp')
    press = aio.feeds('press')
    alt = aio.feeds('alt')
except RequestError: # create a digital feed
    feed = Feed(name="rain")
    rain = aio.create_feed(feed)

rain_sensor = Button(6)
BUCKET_SIZE = 2
count = 0

def bucket_tipped():
    global count
    count = count + 1
    return (rainfall)

def connect():
    try:
        urllib.request.urlopen('http://google.com') #Python 3.x
        return True
    except:
        return False

while True:
    if connect() is True:
        cTemp, pressure, altitude = bmpsensor.readBmp180()
        rain_sensor.when_pressed = bucket_tipped
        rainfall = count * BUCKET_SIZE
        iso = time.ctime()
        print ("Time now : %s " %iso)
        print ("Rain : %.2f " %rainfall)
        print ("Altitude : %.2f m" %altitude)
        print ("Pressure : %.2f hPa " %pressure)
        print ("Temperature in Celsius : %.2f C" %cTemp)
        print ("connected" if connect() else "no internet!")
        aio.send(rain.key, rainfall)
        aio.send(bmptemp.key, cTemp)
        aio.send(press.key, pressure)
        aio.send(alt.key, altitude)
        data = [
        {
          "measurement": measurement,
              "tags": {
                  "location": location,
              },
              "time": time.ctime(),
              "fields": {
                  "temperature" : cTemp,
                  "altitude": altitude,
                  "pressure": float(pressure),
                  "rainfall": rainfall
              }
          }
        ]
        # Send the JSON data to InfluxDB
        client.write_points(data)
        
        # avoid timeout from adafruit io
        time.sleep(10)
    else:
        print ("no internet!")
        time.sleep(60)
