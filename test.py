import os
import datetime
today = datetime.date.today()
now = datetime.datetime.now()
if not os.path.exists('screenshots/sas/залупа 1'):
    os.makedirs('screenshots/sas/залупа 1')
print(today)
# os.makedirs('залупа1')

# print(os.getcwd())

# for i in range(1,)

dif = datetime.timedelta(hours=3)

print(now)
print(now + dif)
