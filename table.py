import PySimpleGUI as sg
import csv

menu_def = [['File', ['Open', 'Save', 'Exit']],
            ['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],
            ['Help', 'About...'],]

sg.SetOptions(element_padding=(0,0))
layout = [ [sg.Menu(menu_def)],
           [sg.T('Table Using Combos and Input Elements', font='Any 18')],
          [sg.T('Row, Cal to change'),
           sg.In(key='inputrow', justification='right', size=(8,1), pad=(1,1), do_not_clear=True),
           sg.In(key='inputcol', size=(8,1), pad=(1,1), justification='right', do_not_clear=True),
           sg.In(key='value', size=(8,1), pad=(1,1), justification='right', do_not_clear=True)]]

for i in range(20):
    inputs = [sg.In(size=(18, 1), pad=(1, 1), justification='right', key=(i,j), do_not_clear=True) for j in range(10)]
    line = [sg.Combo(('Customer ID', 'Customer Name', 'Customer Info'))]
    line.append(inputs)
    layout.append(inputs)

form = sg.FlexForm('Table', return_keyboard_events=True, grab_anywhere=False)
form.Layout(layout)

while True:
    button, values = form.Read()
    if button is None:
        break
    if button == 'Open':
        filename = sg.PopupGetFile('filename to open', no_window=True, file_types=(("CSV Files","*.csv"),))
        if filename is not None:
            with open(filename, "r") as infile:
                reader = csv.reader(infile)
                # first_row = next(reader, None)  # skip the headers
                data = list(reader)  # read everything else into a list of rows
                sg.Print(data)
                for i, row in enumerate(data):
                    for j, item in enumerate(row):
                        print(i,j, item)
                        # form.FindElement(key=(i,j)).Update(item)
                        location = (i,j)
                        try:
                            # location = (int(values['inputrow']), int(values['inputcol']))
                            target_element = form.FindElement(location)
                            new_value = item
                            # new_value = values['value']
                            if target_element is not None and new_value != '':
                                target_element.Update(new_value)
                        except:
                            pass
    if button == 'Exit':
        break
    try:
        location = (int(values['inputrow']), int(values['inputcol']))
        target_element = form.FindElement(location)
        new_value = values['value']
        if target_element is not None and new_value != '':
            target_element.Update(new_value)
    except:
        pass