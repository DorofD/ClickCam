import os
import datetime
today = datetime.date.today()

if not os.path.exists('screenshots/sas/залупа 1'):
    os.makedirs('screenshots/sas/залупа 1')
print(today)
# os.makedirs('залупа1')

print(os.getcwd())
