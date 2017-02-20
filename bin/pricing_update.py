#!/usr/bin/python
import time
import subprocess
import shutil
from os import system,listdir,unlink

basedir = '/home/pi/pricing'
activedir = "%s/activepricing" % basedir
dirlist = {'Sat':"%s/saturdaypricing" % basedir,
        'weekday':"%s/weekdaypricing" % basedir,
        'weeknight':"%s/weeknightpricing" % basedir,
        'holiday':"%s/holidaypricing" % basedir,
        'thunder':"%s/thunderpricing" % basedir,
        }
holiday_list = {
  2 : [20],
  5 : [29],
  7 : [4],
  9 : [4],
  11 : [10,23,24],
  12 : [24,25,31],
  1 : [1],
    }

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
if curday in ['Fri','Sat'] and int(time.strftime("%H", time.localtime())) in [22,23,24,0,1,2,3,4]:
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

feh_check = subprocess.check_output(["ps","aux"])
if feh_check.count("feh") == 0:
    subprocess.call(["%s/bin/start_pricing.sh" % basedir])
