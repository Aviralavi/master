import os

import schedule
import sys
import time
from flaskpackage.routes.route_delete import errors

from flaskpackage import model, run_process_main

kill_value_start = [1]

def store_bookmark_start_schedule():
    global bookmarks_start_schedule
    bookmarks_start_schedule = []
    getAllData = model.StartTable.query.all()
    alldateLength = len(getAllData)
    for datarange in range(0, alldateLength):
        getAllDataString = str(getAllData[datarange])
        containAlldataDict = getAllDataString.split(":::")
        bookmarks_start_schedule.append(dict({containAlldataDict[0]: [containAlldataDict[1], containAlldataDict[2]]}))

def store_error(error):
    errors.append(error)
try:
    def action_schedule_start():
        store_error("Schedule start process started")
        store_bookmark_start_schedule()
        for delete_main_pass in bookmarks_start_schedule:
            for get_key, get_val in delete_main_pass.items():
                if os.path.exists(get_val[0]) == True:
                    if get_val[1] == '':
                        run_process_main.startProgram(get_val[0])
                        store_error("Starting process '{}'".format(get_key))
                    if get_val[1] != '':
                        run_process_main.start_thread(get_val[0], get_val[1])
                        store_error("Starting process '{}'".format(get_key))
                else:
                    store_error("'{}' does not exist".format(get_val[0]))
except Exception as e:
    store_error(e)

def call_with_timer_start(time_start):
    global kill_value_start
    kill_value_start = [1]
    schedule.every().day.at(time_start).do(action_schedule_start)

    while True:
        if kill_value_start[-1] != 0:
            schedule.run_pending()
            time.sleep(1)
        else:
            store_error("Schedule stopped")
            sys.exit()
