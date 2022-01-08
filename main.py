import UI_v4 as UI
import PySimpleGUI as sg

        
'''
    TOOD:
        Implement Save\Load Settings
        Reset DDS
        Organizing
        
'''

def main():
    UI.draw_subplot()
    while True:
        event, values = mainWindow.read(timeout=1)
        a = UI.event_values(event, values)
        if a == -1:
            break
    mainWindow.close()

if __name__ == '__main__':
    mainWindow = UI.main_window()
    UI._VARS['window'] = mainWindow
    main()
