#!/home/scott/Desktop/PythonScripts/dev-venv/bin/python3
from  mfrc522 import SimpleMFRC522
import time

#Start the scanner
scanner = SimpleMFRC522()
print("Scanner is Online")

#Try/catch function to catch an errors from the scanner
try:
    #Read in the victim Card
    print("Please scan the card you wish to clone")
    id,text = scanner.read()
    if id:
        print("Chip ID: {}".format(id))
        print("Chip data: {}".format(text));
    else:
        print("No tag")
    time.sleep(2)
    #Write the data to the attacker card
    print("Please scan the card you wish to clone to")
    id, textWritten = scanner.write(text)
    print("Card cloned succesfully")
except KeyboardInterrupt:
    print("Closing Scanner")
finally: 
    import RPi.GPIO as GPIO
    GPIO.cleanup()



