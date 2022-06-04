from datetime import datetime
import calendar

arr = ['2022-6-24','2022-6-23','2022-6-21' ]
task_name=['Brinks (Tuesday)']
word = 'Tuesday'
tuesday = ''    

for i in range(len(arr)) :
    Myday= datetime.strptime(arr[i], '%Y-%m-%d').date()
    if word in task_name[0]:
        tuesday = "Tuesday"
    if calendar.day_name[Myday.weekday()] == tuesday:
        print(True)
    else:
        print(False)
