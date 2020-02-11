import thingspeak
import time
import Adafruit_DHT
 
channel_id = 970724 
write_key  = 'I816GVMOX4GSWWLJ' 
read_key   = 'GN4DEPT2WV7PNJ8O' 
pin1 = 4
pin2 = 10
sensor = Adafruit_DHT.DHT22

# offset last values with values from pin1
lasthumidity, lasttemperature = Adafruit_DHT.read_retry(sensor, pin1)
 
def measure(channel):
    try:
        humidity1, temperature1 = Adafruit_DHT.read_retry(sensor, pin1)
        humidity2, temperature2 = Adafruit_DHT.read_retry(sensor, pin2)

        averagetemperature = (temperature1 + temperature2) / 2
        averagehumidity = (humidity1 + humidity2) / 2

        # if the temp is higher than 50 or lower than 10, the value can not be right
        if (averagetemperature <= 50) & (averagetemperature >= 10): 
            temperature = averagetemperature 
        else:
            temperature = lasttemperature
        # if the humidity is higher than 80 or lower than 20, the value can not be right
        if (averagehumidity <= 80) & (averagehumidity >= 10): 
            humidity = averagehumidity 
        else:
            humidity = lasthumidity

        # write
        response = channel.update({'field1': temperature, 'field2': humidity})
        
        # read
        read = channel.get({})
        print("written")

        # save values 
        lasttemperature = temperature
        lasthumidity = humidity
        
    except:
        print("connection failed")
 
 
if __name__ == "__main__":
    channel = thingspeak.Channel(id=channel_id, write_key=write_key, api_key=read_key)
    while True:
        measure(channel)
        time.sleep(60)

