"""
'barometro'
==================================
Barometro e Temometro BMP180.
Envia as informaçoes na dashboard
adafruit.io e salva as informaçoes
na db influx.

Autor: G.Goulart
"""
# Import standard python modules
import time

import bmpsensor
# import Adafruit Blinka
import board
import digitalio

# import Adafruit IO REST client.
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
measurement = "bmp180"
# location will be used as a grouping tag later
location = "sede"

try: # if we have a 'digital' feed
    bmptemp = aio.feeds('bmptemp')
    press = aio.feeds('press')
    alt = aio.feeds('alt')
except RequestError: # create a digital feed
    feed = Feed(name="bmptemp")
    bmptemp = aio.create_feed(feed)


while True:
    cTemp, pressure, altitude = bmpsensor.readBmp180()
    print ("Altitude : %.2f m" %altitude)
    print ("Pressure : %.2f hPa " %pressure)
    print ("Temperature in Celsius : %.2f C" %cTemp)
    aio.send(bmptemp.key, cTemp)
    aio.send(press.key, pressure)
    aio.send(alt.key, altitude)
    dados = [
    {
      "measurement": measurement,
          "tags": {
              "location": location,
          },
          "time": time.ctime(),
          "fields": {
              "temperature" : cTemp,
              "altitude": altitude,
              "pressure": float(pressure)
          }
      }
    ]
    # Send the JSON data to InfluxDB
    client.write_points(dados)
    # avoid timeout from adafruit io
    time.sleep(10)
