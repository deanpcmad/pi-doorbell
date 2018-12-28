# import the necessary packages
import time
from time import gmtime, strftime
import sys, os
import RPi.GPIO as GPIO
import requests

GPIO.setwarnings(False)

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use
# Physical pins 12
# GPIO18
pin_button = 18
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# allow the camera to warmup
time.sleep(0.5)
i=0
while True:
    input_state = GPIO.input(pin_button) # Sense the button

    if input_state == False:
        filename = strftime("%Y-%m-%d_%H-%M-%S", gmtime()) + ".jpg"
        #os.system("fswebcam -r 1920X1080 -S 15 image_" + str(i) +".jpg")
        #time.sleep(0.3)
        #i += 1

        GPIO.setup(23,GPIO.OUT)
        print "LED on"
        GPIO.output(23,GPIO.HIGH)
        #time.sleep(0.5)
        #print "LED off"
        #GPIO.output(23,GPIO.LOW)

        os.system('aplay doorbell.wav &')

        os.system("fswebcam -r 1920X1080 -S 5 " + filename)
        time.sleep(0.3)

        # send notification
        url = 'https://api.pushover.net/1/messages.json'
        data  = {'token': '', 'user': '', 'message': 'Someone has rung the door', 'sound': 'echo'}
        files = {'attachment': (filename, open(filename, 'rb'), 'image/jpeg', {'Expires': '0'})}

        r = requests.post(url, data=data, files=files)
        print(r.status_code, r.reason)
        print(r.text)

        i += 1

        #os.system('aplay dingdong.wav')

        GPIO.output(23,GPIO.LOW)
