import RPi.GPIO as GPIO  
from time import sleep     # this lets us have a time delay (see line 12)  
GPIO.setmode(GPIO.BOARD)     # set up BCM GPIO numbering  
button_pin = 40
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # set GPIO 25 as input  

try:  
    while True:            # this will carry on until you hit CTRL+C  
        if GPIO.input(40): # if port 25 == 1  
            print("Port 40 is 1/GPIO.HIGH/True - button pressed")
        else:  
            print("Port 40 is 0/GPIO.LOW/False - button not pressed")
        sleep(0.1)         # wait 0.1 seconds  
  
except KeyboardInterrupt:  
    GPIO.cleanup()         # clean up after yourself  