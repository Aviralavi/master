import schedule
import time
import sys
from flaskpackage import model, cmd_execution
from flaskpackage.routes.route_delete import errors

kill_value_exe = [1]
bookmarks_exe_schedule = []

def store_bookmark_exe_schedule(prof="xxxyyyzzz1234!@#$r"):
    global bookmarks_exe_schedule
    bookmarks_exe_schedule = []
    get_commands = model.ExecuteTable.query.filter_by(name = prof).all()
    for datarange in range(0, len(get_commands)):
        getAllDataString = str(get_commands[datarange])
        containAlldataDict = getAllDataString.split(":::")
        bookmarks_exe_schedule.append(dict({containAlldataDict[0]: list(map(lambda x: x, containAlldataDict[1:]))}))

def store_error(error):
    errors.append(error)

try:
    def call_schedule_execute(get_call_exe):
        store_error("Schedule execution started")
        store_bookmark_exe_schedule(get_call_exe)
        for ind in bookmarks_exe_schedule:
            cmd_execution.batch_cmd = []
            for z, y in ind.items():
                cmd_execution.get_commands(y)
except Exception as e:
    store_error(e)

def call_with_timer_exe(time_run, get_call_exe):
    global kill_value_exe
    kill_value_exe = [1]
    schedule.every().day.at(time_run).do(call_schedule_execute, get_call_exe)

    while True:
        if kill_value_exe[-1] != 0:
            schedule.run_pending()
            time.sleep(1)
        else:
            store_error("Schedule stopped")
            sys.exit()
