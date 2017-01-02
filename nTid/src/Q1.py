
from datetime import date
from datetime import timedelta

# Today
datToday = date.today()
print "Today",str(type(datToday)),datToday

# First Day of This Week
datFirstDayofThisWeek = datToday - timedelta(days=datToday.timetuple()[6]) # i.e. most recent Monday
print "First day of This Week",datFirstDayofThisWeek

# First Day of Last Week
datFirstDayofLastWeek = datFirstDayofThisWeek - timedelta(weeks=1)
print "First day of Last Week",datFirstDayofLastWeek

# First Day of This Month
datFirstDayofThisMonth = datToday.replace(day=1)
print "First day of This Month",datFirstDayofThisMonth

# First Day of Last Month - Is less straight forward... :-(
y = datToday.year
m = datToday.month
d = 1
if m == 1:
    y -= 1
    m = 12
else:
    m -= 1
datFirstDayofLastMonth = date(y,m,d)              
print "First day of Last Month",datFirstDayofLastMonth


