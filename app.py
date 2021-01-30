from threading import current_thread
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Window

'''
sg.theme('BluePurple')

layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(15,1), key='-OUTPUT-')],
          [sg.Input(key='-IN-')],
          [sg.Button('Show'), sg.Button('Exit')]]

window = sg.Window('Pattern 2B', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])

window.close()
'''


get_date_layout =   [
                        [
                            sg.Text('Enter Today\'s Date')
                        ],[   
                            sg.Listbox(values=[i for i in range(1, 32)], size=(5, 3), key='DATE'), 
                            sg.Listbox(values=[i for i in range(1, 13)], size=(5, 3), key='MONTH'), 
                            sg.Listbox(values=[i for i in range(2021, 2050)], size=(5, 3), key='YEAR')
                        ],[
                            sg.Text('select the shift'), sg.Listbox(values=['P1', 'P3'], key='SHIFT', size=(5, 3))
                        ]
                    ]

select_files_layout =   [
                            [
                                sg.Button('select planned file', key='BT_PLAN'), sg.Text('', key='FILENAME1', size=(20,1))
                            ],[
                                sg.Button('select employees file', key='BT_EMP'), sg.Text('', key='FILENAME2', size=(20, 1))
                            ]
                        ]

employee_layout =   [
                        [
                            sg.Text('Employee ID'), sg.InputText('', key='EMP_ID'), sg.Button('Show', key='BT_SHOW')
                        ],[
                            sg.Text('', key='EMP_DETAILS')
                        ]
                    ]

# manage the layouts
layouts =   [
                [
                    sg.Column(get_date_layout, key='COL1'), 
                    sg.Column(select_files_layout, visible=False, key='COL2'),
                    sg.Column(employee_layout, visible=False, key='COL3')
                ],[
                    sg.Button('back', key='BT_BACK', visible=False), 
                    sg.Button('next', key='BT_NEXT'), 
                    sg.Exit()
                ]
            ]
current_layout = 1
max_layout = 3

# date and shift details
date = ''
month = ''
year = ''
shift = ''

# file names
planned_file = ''
employees_file = ''

window = sg.Window('Attendance', layouts, size=(640, 480), element_justification='center')

while True:
    event, values = window.read()

    print(event, values, current_layout)
    
    if current_layout == 1:
        date = window['DATE'] if window['DATE'] else ''
        month = window['MONTH'] if window['MONTH'] else ''
        year = window['YEAR'] if window['YEAR'] else ''
        shift = window['SHIFT'] if window['SHIFT'] else ''

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'BT_NEXT':
        if current_layout == 1:
            window['BT_BACK'].update(visible=True)
        if current_layout+1 == max_layout:
            window['BT_NEXT'].update(visible=False)


        window[f'COL{current_layout}'].update(visible=False)
        current_layout += 1
        window[f'COL{current_layout}'].update(visible=True)

    if event == 'BT_BACK':
        window[f'COL{current_layout}'].update(visible=False)
        current_layout -= 1
        window[f'COL{current_layout}'].update(visible=True)

        if current_layout == 1:
            window['BT_BACK'].update(visible=False)
        if current_layout != max_layout:
            window['BT_NEXT'].update(visible=True)

    if event == 'BT_PLAN':
        planned_file = sg.popup_get_file('Select the planned file')
        window['FILENAME1'].update(planned_file.split('/')[-1])

    if event == 'BT_EMP':
        employees_file = sg.popup_get_file('Select the employees file')
        window['FILENAME2'].update(employees_file.split('/')[-1])

window.close()