import schedule
import time
import sys
from flaskpackage import model, deleteMain
from flaskpackage.routes.route_delete import errors

bookmarks_del_schedule = []
kill_value_delete = [1]

def store_error(error):
    errors.append(error)


def store_bookmark_del_schedule():
    global bookmarks_del_schedule
    bookmarks_del_schedule = []
    getAllData = model.DeleteTable.query.all()
    alldateLength = len(getAllData)
    for datarange in range(0, alldateLength):
        getAllDataString = str(getAllData[datarange])
        containAlldataDict = getAllDataString.split(":::")
        bookmarks_del_schedule.append(dict({containAlldataDict[0]: containAlldataDict[1]}))


def action_scheduler_delete():
    store_error("Schedule delete started")
    store_bookmark_del_schedule()
    for delete_main_pass in bookmarks_del_schedule:
        for get_key, get_val in delete_main_pass.items():
            try:
                deleteMain.deleteFiles(get_val)
                store_error("'{}\*' deleted successfully".format(get_val))
            except Exception as e:
                store_error(e)

def call_with_timer_delete(time_start):
    global kill_value_delete
    kill_value_delete = [1]
    schedule.every().day.at(time_start).do(action_scheduler_delete)

    while True:
        if kill_value_delete[-1] != 0:
            schedule.run_pending()
            time.sleep(1)
        else:
            store_error("Schedule stopped")
            sys.exit()
