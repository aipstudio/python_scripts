#pip install pypiwin32, ntplib
import datetime
from threading import Timer
from datetime import timedelta
import win32api
import ntplib
from datetime import datetime, timezone

def run():
  Timer(300,run).start()
  cur_date_local = datetime.utcnow()
  c = ntplib.NTPClient()
  response = c.request('91.206.16.3', version=3)
  response.offset
  cur_date_ntp = datetime.fromtimestamp(response.tx_time, timezone.utc)
  delta = cur_date_ntp + timedelta(days=10)
  if cur_date_ntp.date() <= cur_date_local.date():
    win32api.SetSystemTime(delta.year, delta.month, 0, delta.day,
      delta.hour, delta.minute, delta.second, delta.microsecond//1000)
    print(str(cur_date_local) + ' time set +10 days')

run()
