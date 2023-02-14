import PySimpleGUI as Sg
import RPi.GPIO as GPIO
import ui.app as app
from event_handlers.events import event_handler
from funcs.las_funcs import turn_off_all_lasers

GPIO.setmode(GPIO.BOARD)
app = app.MainApplication()

while True:
    event, values = app.read()
    if event not in ['__TIMEOUT__', Sg.WIN_CLOSED]:
        a = event_handler(app, event, values)
    if event == Sg.WIN_CLOSED:
        turn_off_all_lasers()
        break

app.close()
