import csv
import pandas as pd

date = input("Enter date : ")
shift = input("Enter shift : ")

attendance_filename = input("Enter the attendance file name : ")
input("continue ?")

planned = pd.read_csv(attendance_filename)
planned = planned.astype({'Emp id': 'string'})
planned.set_index("Emp id", inplace=True)
date_present = planned.columns.get_loc(date)+1
date_present = planned.columns[date_present]

planned[date_present] = planned[date_present].fillna('A')

present = pd.DataFrame(columns=['id'])

c = 'a'
while c != 'q':
    eid = input("Enter employee id : ")
    present.append(pd.DataFrame([[eid]], columns=['id']), ignore_index=True)
    print(present)
    planned.loc[eid, date_present] = shift
    c = input()

    planned.reset_index()
    planned.to_csv(attendance_filename)
    present.to_csv('{}:{}.csv'.format(date, shift))
    print(planned.columns)
    planned.set_index("Emp id", inplace=True)

print(planned)

