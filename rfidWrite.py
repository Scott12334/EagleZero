#!/home/scott/Desktop/PythonScripts/dev-venv/bin/python3
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

scanner = SimpleMFRC522()

try:
    text = "Hacker Card"
    id, textWritten = scanner.write(text)
    print("Done")
    time.sleep(1)
    text = "ID:Scott Nicholson 4856"
    id, textWritten = scanner.write(text)
    print("Done")
finally:
    GPIO.cleanup()
