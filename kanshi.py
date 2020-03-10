# coding:utf-8
#!/usr/bin/python3
from subprocess import Popen
import threading
import schedule
import time
import os

print("AppStart")

current_dir = os.path.dirname(os.path.abspath(__file__))

def alert():
    cmd = "python3 command/alert.py"
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
    cmd = "python3 command/bot.py"
    proc = Popen(cmd.strip().split(" "))
    proc.wait()


def command5():
    cmd = "python3 command/role.py"
    proc = Popen(cmd.strip().split(" "))
    proc.wait()


def command7():
    cmd = "python3 command/squad.py"
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
