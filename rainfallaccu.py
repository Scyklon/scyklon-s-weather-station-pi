import time
import sys
import datetime
from gpiozero import Button
from influxdb import InfluxDBClient

# Configure InfluxDB connection variables
host = "localhost" # My Ubuntu NUC
port = 8086 # default port
user = "" # the user/password created for the pi, with write access
password = "" 
dbname = "telegraf" # the database we created earlier
interval = 60 # Sample period in seconds

# Create the InfluxDB client object
client = InfluxDBClient(host, port, user, password, dbname)

# Enter the sensor details
rain_sensor = Button(6)
BUCKET_SIZE = 2
count = 0

def bucket_tipped():
    global count
    count = count + 1
    print(count * BUCKET_SIZE)
    
def reset_rainfall():
    global count
    count = 0

# think of measurement as a SQL table, it's not...but...
measurement = "rainfallaccu"
# location will be used as a grouping tag later
location = "sede"

# Run until you get a ctrl^c
try:
    while True:
        # Read the sensor using the configured driver and gpio
        rain_sensor.when_pressed = bucket_tipped
        rainfall = count * BUCKET_SIZE
        iso = time.ctime()
        # Print for debugging, uncomment the below line
        print("[%s] rainfall %s" % (iso, rainfall)) 
        # Create the JSON data structure
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
        # Wait until it's time to query again...
        time.sleep(interval)
 
except KeyboardInterrupt:
    pass

