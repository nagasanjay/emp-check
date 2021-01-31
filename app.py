from threading import current_thread
from tkinter.constants import DISABLED
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Window
import pandas as pd

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
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

get_date_layout =   [
                        [
                            sg.Text('Enter Today\'s Date')
                        ],[   
                            sg.Listbox(values=[i for i in range(1, 32)], size=(5, 3), key='DATE'), 
                            sg.Listbox(values=months, size=(5, 3), key='MONTH'), 
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
                    sg.Button('back', key='BT_BACK', disabled=True), 
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

today = ''

# file names
planned_file = ''
employees_file = ''

# ------ backend functions -------
# initialize the local db
def initialize(date, attendance_filename):
    planned = pd.read_csv(attendance_filename)
    planned = planned.astype({'Emp id': 'string'})
    planned['index'] = planned['Emp id']
    planned.set_index("index", inplace=True)
    date_present = planned.columns.get_loc(date)+1
    date_present = planned.columns[date_present]
    planned[date_present] = planned[date_present].fillna('A')
    present = pd.DataFrame(columns=['id'])
    return planned,date_present,present

init = False
planned = ''
date_present = ''
present = ''

# mark attendance
def put_attendance(date, shift, attendance_filename, planned, date_present, present, eid):
    print(eid)
    present.append(pd.DataFrame([[eid]], columns=['id']), ignore_index=True)
    print(present)
    planned.loc[eid, date_present] = shift
    planned.reset_index()
    planned.to_csv(attendance_filename)
    present.to_csv('{}:{}.csv'.format(date, shift))
    print(planned.columns)
    planned['index'] = planned['Emp id']
    planned.set_index("Emp id", inplace=True)

window = sg.Window('Attendance', layouts, size=(640, 480), element_justification='center')

while True:
    event, values = window.read()

    print(event, values, current_layout)

    if init == False and current_layout == max_layout:
        init = True
        planned, date_present, present = initialize(today, planned_file)
    
    if current_layout == 1:
        date = str(values['DATE'][0]) if window['DATE'] else ''
        month = values['MONTH'][0] if window['MONTH'] else ''
        year = str(values['YEAR'][0]) if window['YEAR'] else ''
        shift = values['SHIFT'][0] if window['SHIFT'] else ''

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'BT_NEXT':
        if current_layout == 1:
            window['BT_BACK'].update(disabled=False)
            today = date+'-'+month
        if current_layout+1 == max_layout:
            window['BT_NEXT'].update(disabled=True)


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

    if event == 'BT_SHOW':
        put_attendance(today, shift, planned_file, planned, date_present, present, values['EMP_ID'])

window.close()