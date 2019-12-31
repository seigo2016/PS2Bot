# coding:utf-8
from subprocess import Popen
import threading
import schedule
import time

s = sched.scheduler(time.time, time.sleep)
sh = datetime.datetime(2020, 1, 1, 0, 0)
sh = int(time.mktime(et2.timetuple()))

def newyear():
    cmd = "python ./command/newyear.py"¬
    proc = Popen(cmd.strip().split(" "))¬
    time.sleep(30)¬
    proc.wait()

s.enterabs(et1, 1, newyear)

def alert():
    cmd = "python ./command/alert.py"
    proc = Popen(cmd.strip().split(" "))
    time.sleep(30)
    proc.terminate()


schedule.every(5).minutes.do(alert)


def command1():
    alert()
    while True:
        schedule.run_pending()
        time.sleep(1)


def command3():
    cmd = "python ./command/bot.py"
    proc = Popen(cmd.strip().split(" "))
    proc.wait()


def command5():
    cmd = "python ./command/role.py"
    proc = Popen(cmd.strip().split(" "))
    proc.wait()


def command7():
    cmd = "python ./command/squad.py"
    proc = Popen(cmd.strip().split(" "))
    proc.wait()


th1 = threading.Thread(target=command1)
th3 = threading.Thread(target=command3)
th5 = threading.Thread(target=command5)
th7 = threading.Thread(target=command7)
th1.start()
th3.start()
th5.start()
th7.start()
