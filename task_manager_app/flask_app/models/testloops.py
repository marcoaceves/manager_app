from datetime import datetime
import calendar

arr = ['2022-6-24','2022-6-23','2022-6-21' ]

for i in range(len(arr)) :

    Myday= datetime.strptime(arr[i], '%Y-%m-%d').date()

    if calendar.day_name[Myday.weekday()] == "Tuesday":
        print(True)
    print(calendar.day_name[Myday.weekday()])