#!/home/scott/Desktop/PythonScripts/dev-venv/bin/python3
from mfrc522 import SimpleMFRC522
import time

try: 
    scanner = SimpleMFRC522()
    print("Scanner is online")
except Exception as e:
    print("Scanner is not working: {e}")
    exit(1)

print("Scan Tag/Card")

try:
    while True:
        id,text = scanner.read()
        text = text.strip()
        if id:
            print("Chip ID: {}".format(id))
            print("Chip Text: {}".format(text));
        else:
            print("No tag")
        if text == "ID:Scott Nicholson 4856":
            print("Welcome home Scott!")
        else:
            print("Unauthorized Access")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Closing Scanner")
finally: 
    import RPi.GPIO as GPIO
    GPIO.cleanup()
