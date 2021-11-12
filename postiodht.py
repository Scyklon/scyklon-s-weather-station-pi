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
import Adafruit_DHT
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
measurement = "rpi-dht22"
# location will be used as a grouping tag later
location = "sede"

try: # if we have a 'digital' feed
    dhttemp = aio.feeds('dhttemp')
    humidity = aio.feeds('humidity')
except RequestError: # create a digital feed
    feed = Feed(name="dhttemp")
    dhttemp = aio.create_feed(feed)
    feed = Feed(name="humidity")
    humidity = aio.create_feed(feed)
# Enter the sensor details
sensor = Adafruit_DHT.DHT11
sensor_gpio = 4

# think of measurement as a SQL table, it's not...but...
measurement = "rpi-dht22"
# location will be used as a grouping tag later
location = "sede"

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)
    iso = time.ctime()
    # Print for debugging, uncomment the below line
    print("[%s] Temp: %s, Humidity: %s" % (iso, temperature, humidity))
    aio.send(rain.key, rainfall)
    data = [
    {
      "measurement": measurement,
          "tags": {
              "location": location,
          },
          "time": iso,
          "fields": {
              "temperature" : temperature,
              "humidity": humidity
          }
      }
    ]
    # Send the JSON data to InfluxDB
    client.write_points(data)
    
    # avoid timeout from adafruit io
    time.sleep(2)