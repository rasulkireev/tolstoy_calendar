import datetime as dt

today = dt.date.today()
date_tuple = today.timetuple()
this_month = date_tuple[1]
this_day = date_tuple[2]

print(f"Today is {this_month} month")