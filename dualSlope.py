import UI
import RPi.GPIO as GPIO

# TODO
# In the lab, see if changing the order of set_freqmult() and set_refclock in funcs.py distorts the channels.
# See if dds.shutdown() and dds.wake_up() works.
# Implement update_fills()
# Look up the GPIO pin numbers for the lasers

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
