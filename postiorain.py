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
ADAFRUIT_IO_KEY = '2905909fbdd8465d847a7a7180ea11cd'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'Scyklon'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# think of measurement as a SQL table, it's not...but...
measurement = "rainfall"
# location will be used as a grouping tag later
location = "sede"

try: # if we have a 'digital' feed
    rain = aio.feeds('rain')
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

while True:
    rain_sensor.when_pressed = bucket_tipped
    rainfall = count * BUCKET_SIZE
    iso = time.ctime()
    print ("Rain : %.2f " %rainfall)
    aio.send(rain.key, rainfall)
    data = [
        {
          "measurement": measurement,
              "tags": {
                  "location": location,
              },
              "time": iso,
              "fields": {
                  "rainfall": rainfall
              }
          }
        ]
    # Send the JSON data to InfluxDB
    client.write_points(data)
    
    # avoid timeout from adafruit io
    time.sleep(10)
