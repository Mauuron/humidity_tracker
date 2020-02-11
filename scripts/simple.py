import thingspeak
import time
import Adafruit_DHT
 
channel_id = your_channel_id
write_key  = 'your_key' 
read_key   = 'your_key' 
pin = your_pin_number
sensor = Adafruit_DHT.DHT22 
 
def measure(channel):
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        
        # write
        response = channel.update({'field1': temperature, 'field2': humidity}) #adjust according to your channel
        
        # read
        read = channel.get({})
        print("written")
        
    except:
        print("connection failed")
 
 
if __name__ == "__main__":
    channel = thingspeak.Channel(id=channel_id, write_key=write_key, api_key=read_key)
    while True:
        measure(channel)
        time.sleep(60) 
