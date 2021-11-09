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
interval = 0 # Sample period in seconds

# Create the InfluxDB client object
client = InfluxDBClient(host, port, user, password, dbname)
recording_time_timeout = 10  # Amount of seconds you want to have the timer run
recording_time = time.monotonic() + recording_time_timeout
button_timeout = 1  # This timeout is here so the button doesnt trigger the count more then once for each trigger
count = 0
button = Button(6)# Sets the counter to 0 at the start
# Here you need to replace the 0 with the GPIO pin that returns True if the button is presse 

# think of measurement as a SQL table, it's not...but...
measurement = "rainfallhour"
# location will be used as a grouping tag later
location = "sede"
def bucket_tipped():
    global count
    count = count + 1

# Run until you get a ctrl^c
try:
    while True:
        if bucket_tipped:         # if button gets pressed/bucket tipped
            button.when_pressed = bucket_tipped
            time.sleep(button_timeout)  # wait specified timeout to make sure button isnt pressed anymore

        if time.monotonic() > recording_time:  # If the recording_time is reached the loop triggers this if condition
            print(count)   # print count
                           # Here you can also place code that you want to run when the hour is over
                           # Note that the counter wont start back up until that code is finished.

            count = 0      # set count back to 0
            recording_time = time.monotonic() + recording_time_timeout  # Set a new timer so the hour can start anew

        rainfallhour = count * 2
        iso = time.ctime()
        # Print for debugging, uncomment the below line
        print("[%s] rainfall %s" % (iso, rainfallhour)) 
        # Create the JSON data structure
        data = [
        {
          "measurement": measurement,
              "tags": {
                  "location": location,
              },
              "time": iso,
              "fields": {
                  "rainfall": rainfallhour
              }
          }
        ]
        # Send the JSON data to InfluxDB
        client.write_points(data)
        # Wait until it's time to query again...
        time.sleep(interval)
        continue   # restart the loop
 
except KeyboardInterrupt:
    pass
