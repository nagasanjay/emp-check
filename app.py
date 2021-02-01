from threading import current_thread
from tkinter.constants import DISABLED
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Column, Window
import pandas as pd
import csv
import os

if not os.path.exists('stats'):
    os.makedirs('stats')

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
        sg.Listbox(values=[i for i in range(1, 32)], size=(5, 10), key='DATE'), 
        sg.Listbox(values=months, size=(5, 10), key='MONTH'), 
        sg.Listbox(values=[i for i in range(2021, 2050)], size=(5, 10), key='YEAR')
    ],[
        sg.Text('select the shift'), sg.Listbox(values=['P1', 'P3'], key='SHIFT', size=(5, 3))
    ]
                    ]

select_files_layout =   [
    [
        sg.Button('select planned file', key='BT_PLAN'), sg.Text('', key='FILENAME1', size=(20,1))
    ],[
        sg.Button('select employees file', key='BT_EMP'), sg.Text('', key='FILENAME2', size=(20, 1))
    ],[
        sg.Button('select record history file', key='BT_HIS'), sg.Text('', key='FILENAME3', size=(20, 1))
    ]
                        ]

employee_layout =   [
    [
        sg.Text('Employee ID'), sg.InputText('', key='EMP_ID'), sg.Button('Show', key='BT_SHOW')
    ],[
        sg.Text('\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n', key='EMP_DETAILS')
    ],[
        sg.Button('show stats', key='BT_STATS')
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
record_history = ''

# ------ backend functions -------
# initialize the local db
def initialize(date, attendance_filename, employees_file, record_history, _emp):
    planned = pd.read_csv(attendance_filename)
    planned = planned.astype({'Emp id': 'string'})

    _emp = planned['Emp id']
    #planned['index'] = planned['Emp id']
    planned.set_index("Emp id", inplace=True)
    date_present = planned.columns.get_loc(date)+1
    date_present = planned.columns[date_present]
    planned[date_present] = planned[date_present].fillna('A')

    record = pd.read_csv(record_history)
    record = record.astype({'Emp id' : 'string'})
    record.set_index('Emp id', inplace=True)

    #record[today] = planned[date_present]
    _ = planned[date_present]
    record.join(_, on=['Emp id'])
    print(record, planned)

    employees = pd.read_csv(employees_file)
    employees = employees.astype({'employee ID': "string"})
    employees.set_index("employee ID", inplace=True)

    return planned,date_present, employees, record, _emp

init = False
planned = ''
date_present = ''
employees = ''
record = ''
_emp = ''

# mark attendance
def put_attendance(shift, attendance_filename, planned, date_present, eid, record, record_history, today):
    planned.loc[eid, date_present] = shift

    record[today] = planned[date_present]

    record.to_csv(record_history)
    planned.to_csv(attendance_filename)

window = sg.Window('Attendance', layouts, size=(640, 480), element_justification='center')

def display_details(employees, window, values):
    eid = values['EMP_ID']
    details = employees.loc[eid]
    window['EMP_DETAILS'].update(details['employee name']+'\n'+details['task'])
    

def get_stats(shift, today, planned, date_present, _emp):
    _planned = planned[today]
    _present = planned[date_present]
    C_PLANNED = 0
    C_PRESENT = 0
    C_ABSENT = 0
    empids = []

    _shift = '1st' if shift == 'P1' else '3rd'

    '''
    for p in _planned:
        if p == _shift:
            C_PLANNED += 1
    for p in _present:
        if p == shift:
            C_PRESENT += 1
        elif p == 'A':
            C_ABSENT += 1
    '''

    for i in range(len(_planned)):
        if _planned[i] == _shift:
            C_PLANNED += 1
            if _present[i] == 'A':
                C_ABSENT += 1
        if _present[i] == shift:
            C_PRESENT += 1
            empids.append(_emp[i])

    return C_PLANNED, C_PRESENT, C_ABSENT, empids

while True:
    event, values = window.read()

    print(event, values, current_layout)

    if init == False and current_layout == max_layout:
        init = True
        planned, date_present, employees, record, _emp = initialize(
                        today, planned_file, employees_file, record_history, _emp)
    
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
        try:
            planned_file = sg.popup_get_file('Select the planned file')
            window['FILENAME1'].update(planned_file.split('/')[-1])
        except:
            pass

    if event == 'BT_EMP':
        try:
            employees_file = sg.popup_get_file('Select the employees file')
            window['FILENAME2'].update(employees_file.split('/')[-1])
        except:
            pass

    if event == 'BT_HIS':
        try:
            record_history = sg.popup_get_file('Select the record history file')
            window['FILENAME3'].update(record_history.split('/')[-1])
        except:
            pass

    if event == 'BT_SHOW':
        put_attendance(shift, planned_file, planned, date_present, 
                        values['EMP_ID'], record, record_history, today)
        display_details(employees, window, values)

    if event == 'BT_STATS':
        C_PLANNED, C_PRESENT, C_ABSENT, empids = get_stats(shift, today, planned, date_present, _emp)

        with open('{}.csv'.format('stats\\'+shift+'-'+today+'-'+year), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Planned', C_PLANNED])
            writer.writerow(['Present', C_PRESENT])
            writer.writerow(['Absent', C_ABSENT])
            writer.writerow(['Absent percentage', C_ABSENT/C_PLANNED*100])
            writer.writerow(['',''])

        dic = {}

        for id in empids:
            ind = employees.loc[id, 'task']
            print(ind)
            if ind in dic.keys():
                dic[ind] += 1
            else:
                dic[ind] = 1

        with open('{}.csv'.format('stats\\'+shift+'-'+today+'-'+year), 'a', newline='') as file:
            writer = csv.writer(file)
            for item in dic.items():
                writer.writerow([item[0], item[1]])

window.close()