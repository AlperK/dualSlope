import ui.app as app
import RPi.GPIO as GPIO
import PySimpleGUI as Sg
from events import event_handler

# TODO

GPIO.setmode(GPIO.BOARD)
app = app.MainApplication()

while True:
    event, values = app.read()
    if event not in ['__TIMEOUT__', Sg.WIN_CLOSED]:
        # print(f'event: {event}, value: {values[event]}')
        a = event_handler(app, event, values)
    # print(event)
    # if a == -1:
    #     break
    if event == Sg.WIN_CLOSED:
        active_pins = []
        for i in range(1, 41):
            if i not in [1, 2, 4, 6, 9, 14, 17, 20, 25, 27, 28, 30, 34, 39]:
                if GPIO.gpio_function(i) is not -1:
                    active_pins.append(i)

        cleanup_pins = [pin for pin in active_pins if pin not in [10, 13, 15, 16]]
        GPIO.cleanup(cleanup_pins)

        break

app.close()
