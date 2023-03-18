import datetime

key = "qwertrty"

first_time = datetime.datetime(2023, 3, 15, 15, 57, 30)
now = datetime.datetime.now()

if now > first_time:
    key = "0"


print(key)

