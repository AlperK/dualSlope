import UI
import RPi.GPIO as GPIO

# TODO
# See if dds.shutdown() and dds.wake_up() works.
# Find a smart way to trim the 'measurement conditions.json'
# Think about a good structure for the final csv file contains the measurement results

GPIO.setmode(GPIO.BOARD)
app = UI.MainApplication()

while True:
    event, values = app.read(timeout=0)
    a = UI.event_values(app, event, values)
    # print(event)
    if a == -1:
        break

GPIO.cleanup()
app.close()
