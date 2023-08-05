# This file can be used as an UDF for Apache Hive to add months to a date value.
# Holds good for Hive version 0.13 and lesser

import sys
from dateutil.relativedelta import relativedelta
import datetime
import calendar
from calendar import monthrange

# This module will parse all the input lines from Hive and add two months
# to its date values
for line in sys.stdin:
 strip_newline=line.rstrip('\\n')
 vals=strip_newline.strip().split('\\t')
 date_val=vals[0]
 mon_adjust=vals[1]
 if date_val != '\\N':
  cols=date_val.strip().split('-')
  yr=cols[0]
  mon=cols[1]
  dy=cols[2]
  act_dt=datetime.date(int(yr), int(mon), int(dy))
  last_day=calendar.monthrange(int(yr), int(mon))[1]
  if last_day == int(dy):
   rel_mon = relativedelta(months=int(mon_adjust))
   rev_dt=act_dt+rel_mon
   yr1=rev_dt.year
   mon1=rev_dt.month
   last1=calendar.monthrange(int(yr1), int(mon1))[1]
   final_dt=datetime.date(int(yr1), int(mon1), int(last1))
   print (date_val + '\\t' + final_dt.strftime("%Y-%m-%d"))
  else:
   rel_mon = relativedelta(months=int(mon_adjust))
   rev_dt=act_dt+rel_mon
   print (date_val + '\\t' + rev_dt.strftime("%Y-%m-%d"))
 else:
  print ('\\N' + '\\t' + '\\N')
