import ui.app as app
import RPi.GPIO as GPIO
import PySimpleGUI as Sg


GPIO.setmode(GPIO.BOARD)
app = app.MainApplication()

while True:
    event, values = app.read(timeout=0)
    if event not in ['__TIMEOUT__', Sg.WIN_CLOSED]:
        print(f'event: {event}, value: {values[event]}')
    # a = UI.event_values(app, event, values)
    # print(event)
    # if a == -1:
    #     break
    if event == Sg.WIN_CLOSED:
        break

GPIO.cleanup()
app.close()
