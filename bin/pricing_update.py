#!/usr/bin/python
import time
import subprocess
import shutil
from sys import exit
from os import system,listdir,unlink
try:
    import config as cfg
except:
    print 'Config file missing, you should copy config.py.sample to config.py'
    exit(0)

basedir = '/home/pi/pricing'
activedir = "%s/activepricing" % basedir
dirlist = {'Sat':"%s/saturdaypricing" % basedir,
        'weekday':"%s/weekdaypricing" % basedir,
        'weeknight':"%s/weeknightpricing" % basedir,
        'holiday':"%s/holidaypricing" % basedir,
        'thunder':"%s/thunderpricing" % basedir,
        }
#holiday_list = {
#  2 : [20],
#  5 : [29],
#  7 : [4],
#  9 : [4],
#  11 : [10,23,24],
#  12 : [24,25,31],
#  1 : [1],
#    }
## set to true to intersperse images from the alternates folder
#include_alternates = True
holiday_list = cfg.holiday_list
include_alternates = cfg.include_alternates

# begin processing
is_holiday = False
try:
  holiday_list[time.localtime().tm_mon]
  is_holiday = time.localtime().tm_mday in holiday_list[time.localtime().tm_mon]
except:
  pass

af = open("%s/var/current.pid" % basedir, "r")
activep = af.readline().strip()
af.close()

curday = time.strftime("%a",time.localtime())
dealday = time.strftime("%a",time.localtime()).lower()
if curday in ['Fri','Sat','Sun'] and int(time.strftime("%H", time.localtime())) in [22,23,24,0,1,2,3,4]:
    curday = 'thunder'
if curday not in ['Sat','thunder']:
    curday = 'weekday'
    if int(time.strftime("%H", time.localtime())) in [18,19,20,21,22,23,24,0,1,2,3,4]:
        curday = 'weeknight'
if is_holiday:
  curday = 'holiday'

if activep != curday:
    ap = open("%s/var/current.pid" % basedir, "w")
    ap.write(curday)
    ap.close()

    for file in listdir(activedir):
        unlink("%s/%s" % (activedir,file))
    for file in listdir(dirlist[curday]):
        shutil.copy("%s/%s" % (dirlist[curday],file), "%s/%s" % (activedir,file))
    subprocess.call(["killall","feh"])
    if include_alternates:
      alternates_dir = '%s/alternates' % basedir

      if curday == 'weekday':
        alternates_dir = '%s/alternates_weekday' % basedir
      for file in listdir(alternates_dir):
        shutil.copy("%s/%s" % (alternates_dir,file), "%s/%s" % (activedir,file))

try:
    if dealday == "mon":
        shutil.copy("%s/dailydeals/mon.jpg" % (basedir), "%s/mon.jpg" % (activedir))
    elif dealday == "tue" and (int(time.strftime("%H", time.localtime())) not in [19,20,21,22,23,24,0,1,2,3,4]):
        shutil.copy("%s/dailydeals/tue.jpg" % (basedir), "%s/tue.jpg" % (activedir))
    elif dealday == "wed":
        shutil.copy("%s/dailydeals/wed.jpg" % (basedir), "%s/wed.jpg" % (activedir))
    elif dealday == "thu" and (int(time.strftime("%H", time.localtime())) not in [19,20,21,22,23,24,0,1,2,3,4]):
        shutil.copy("%s/dailydeals/thu.jpg" % (basedir), "%s/thu.jpg" % (activedir))
    elif dealday == "fri":
        shutil.copy("%s/dailydeals/fri.jpg" % (basedir), "%s/fri.jpg" % (activedir))
    elif dealday == "sat":
        shutil.copy("%s/dailydeals/sat.jpg" % (basedir), "%s/sat.jpg" % (activedir))
    else:
        pass
except:
    pass

feh_check = subprocess.check_output(["ps","aux"])
if feh_check.count("feh") == 0:
  subprocess.call(["%s/bin/start_pricing.sh" % basedir])
