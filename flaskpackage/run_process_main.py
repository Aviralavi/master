import subprocess
import sys
import threading
import time
from flaskpackage.routes.route_delete import errors

kill_value_start_main = [1]

def store_error(error):
    errors.append(error)


def startProgram(input_file):
    SW_HIDE = 0
    info = subprocess.STARTUPINFO()
    info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = SW_HIDE
    subprocess.call(input_file, shell=True, startupinfo=info)


def thread_distributor(input_file, repeat_time):
    while True:
        if kill_value_start_main[-1] != 0:
            time.sleep(1)
            repeat_time = int(repeat_time)
            startProgram(input_file)
            time.sleep(repeat_time)
        else:
            store_error("Stopped process")
            sys.exit()


def start_thread(input_file, repeat_time):
    global kill_value_start_main
    kill_value_start_main = [1]
    threading.Thread(target=thread_distributor, args=(input_file, repeat_time)).start()
