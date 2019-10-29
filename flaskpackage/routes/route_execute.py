import time
from flask import render_template, url_for, request, redirect
import threading
from flaskpackage import cmd_execution, schedule_execute_main, schedule_delete_main, schedule_start_main
from flaskpackage import model, app, db
from flaskpackage.routes.route_delete import errors
import run

bookmarks_exe = []

profiles = []
schedule_delete_var = []
schedule_execute_var = []
schedule_start_var = []

def store_profile_exe():
    temp_profile = []
    profile_names = [x.name for x in model.ExecuteTable.query.all()]
    for pro in profile_names:
        temp_profile.append(pro)
    global profiles
    profiles = sorted(set(temp_profile))


def store_bookmark(prof="xxxyyyzzz1234!@#$r"):
    global bookmarks_exe
    bookmarks_exe = []
    get_commands = model.ExecuteTable.query.filter_by(name=prof).all()
    for datarange in range(0, len(get_commands)):
        getAllDataString = str(get_commands[datarange])
        containAlldataDict = getAllDataString.split(":::")
        bookmarks_exe.append(dict({containAlldataDict[0]: list(map(lambda x: x, containAlldataDict[1:]))}))


def store_error(error):
    errors.append(error)


try:
    @app.route('/add_profile', methods=['GET', 'POST'])
    def add_profile():
        store_profile_exe()
        if request.method == "POST":
            get_file = request.form.get("name_add_pro", None)

            if get_file != None:
                try:
                    if get_file != "":
                        storeDelValue = model.ExecuteTable(name=get_file, path="")
                        db.session.add(storeDelValue)
                        db.session.commit()
                        store_error("{} added successfully".format(get_file))
                        return redirect(url_for('index'))
                    else:
                        store_error("Empty profile")
                        return render_template("add_profile.html", bookmarks_exe=bookmarks_exe, errors=errors,
                                               profiles=profiles)
                except Exception as e:
                    store_error(e)
                    return render_template("add_profile.html", bookmarks_exe=bookmarks_exe, errors=errors, profiles=profiles)
        return render_template("add_profile.html", bookmarks_exe=bookmarks_exe, errors=errors, profiles=profiles)
except Exception as e:
    store_error(e)

try:
    @app.route('/execute', methods=['GET', 'POST'])
    def execute():
        return render_template("execute.html", bookmarks_exe=bookmarks_exe, errors=errors, profiles=profiles)
except Exception as e:
    store_error(e)

try:
    @app.route('/execute/<string:id>', methods=['GET', 'POST'])
    def execute_profile(id):
        store_bookmark(id)
        store_profile_exe()
        cmd_execution.get_id = [id]
        if request.method == "POST":
            getBookmarkLength = len(bookmarks_exe)
            get_add = request.form.get("addName", None)
            get_file = request.form.get("add_file", None)
            add_all_url = request.form.get("add_all_url", None)
            get_exe_Clicked = request.form.get("deleteClicked", None)
            get_off_exe = request.form.get("off3_name", None)

            if get_off_exe != None:
                cmd_execution.kill_value_exe_main = [0]
                store_error("Stopping execution process")
                return render_template("execute.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                       profiles = profiles, profile_id = id,
                                       pass_fail = cmd_execution.pass_fail)

            if get_exe_Clicked != None:
                try:
                    cmd_execution.kill_value_exe_main = [1]
                    count = 0
                    cmd_execution.pass_fail = []
                    cmd_execution.cwd = []
                    for ind in bookmarks_exe:
                        cmd_execution.batch_cmd = []
                        count += 1
                        for z, y in ind.items():
                            checkval = "check" + str(count)
                            get_check = request.form.get(checkval, "off")
                            get_check_all = request.form.get("click_all", "off")
                            if get_check != "off":
                                try:
                                    cmd_execution.get_commands(y)
                                    cmd_execution.get_log_output()
                                    if get_check_all != "off":
                                        if cmd_execution.pass_fail[-1][id] == "FAIL" or cmd_execution.pass_fail[-1][id] == "ERROR":
                                            return render_template("execute.html", bookmarks_exe=bookmarks_exe, errors=errors, profiles=profiles, profile_id=id, pass_fail=cmd_execution.pass_fail)
                                except Exception as e:
                                    store_error(e)
                                    if get_check_all != "off":
                                        return render_template("execute.html", bookmarks_exe=bookmarks_exe, errors=errors, profiles=profiles, profile_id=id, pass_fail=cmd_execution.pass_fail)
                                    # driver.find_elements_by_link_text("asdf")[0].click()
                            else:
                                cmd_execution.pass_fail.append({id: "N/A"})
                    return render_template("execute.html", bookmarks_exe=bookmarks_exe, errors=errors, profiles=profiles,
                                           profile_id=id, pass_fail=cmd_execution.pass_fail)
                except Exception as e:
                    store_error(e)
                    return render_template("execute.html", bookmarks_exe=bookmarks_exe, errors=errors, profiles=profiles,
                                           profile_id=id, pass_fail=cmd_execution.pass_fail)

            if add_all_url != None:
                try:
                    execute_sql = "DELETE FROM execute_table WHERE name = '{}';".format(id)
                    db.engine.execute(execute_sql)
                    for all in range(getBookmarkLength):
                        get_url = "url" + str(all + 1)
                        get_url_val = request.form.get(get_url, None)
                        storeDelValue = model.ExecuteTable(name=id, path=get_url_val)
                        db.session.add(storeDelValue)
                        db.session.commit()
                    store_bookmark(id)
                    store_profile_exe()
                    return render_template("execute.html", bookmarks_exe=bookmarks_exe, errors=errors, profiles=profiles,
                                           profile_id=id)
                except Exception as e:
                    store_error(e)

            if get_add != None:
                try:
                    store_bookmark(id)
                    return render_template("add_execute.html", bookmarks_exe=bookmarks_exe, errors=errors, profiles=profiles,
                                           profile_id=id)
                except Exception as e:
                    store_error(e)
                    return render_template("add_execute.html", bookmarks_exe=bookmarks_exe, errors=errors, profiles=profiles,
                                           profile_id=id)

            if get_file != None:
                try:
                    get_url = request.form.get("url_add", None)
                    if id != "":
                        storeDelValue = model.ExecuteTable(name=id, path=get_url)
                        db.session.add(storeDelValue)
                        db.session.commit()
                        store_error("Added successfully")
                        store_bookmark(id)
                        return render_template("execute.html", bookmarks_exe=bookmarks_exe, errors=errors, profiles=profiles,
                                               profile_id=id)
                    else:
                        store_error("Profile error")
                        store_bookmark(id)
                        return render_template("add_execute.html", bookmarks_exe=bookmarks_exe, errors=errors,
                                               profiles=profiles, profile_id=id)
                except Exception as e:
                    store_error(e)
                    return render_template("add_execute.html", bookmarks_exe=bookmarks_exe, errors=errors)

            for deleteCount in range(getBookmarkLength):
                try:
                    deleteIMGval = "deleteIMGval" + str(deleteCount + 1)
                    get_delete_logo = request.form.get(deleteIMGval, None)
                    if get_delete_logo != None:
                        get_url = "url" + get_delete_logo
                        get_url = request.form.get(get_url, None)
                        execute_sql = "DELETE FROM execute_table WHERE path = '{}';".format(get_url)
                        db.engine.execute(execute_sql)
                        store_error("Removed successfully")
                        store_profile_exe()
                        print(id)
                        if id in profiles:
                            store_bookmark(id)
                            return render_template("execute.html", bookmarks_exe=bookmarks_exe, errors=errors,
                                                   profiles=profiles, profile_id=id)
                        else:
                            return redirect(url_for('execute'))
                except Exception as e:
                    store_error(e)
        return render_template("execute.html", bookmarks_exe=bookmarks_exe, errors=errors, profiles=profiles, profile_id=id,
                               pass_fail=cmd_execution.pass_fail)

except Exception as e:
    store_error(e)

try:
    @app.route('/', methods=['GET', 'POST'])
    @app.route('/index', methods=['GET', 'POST'])
    def index():
        store_profile_exe()
        global schedule_execute_var
        global schedule_start_var
        global schedule_delete_var
        if request.method == "POST":
            get_delete = request.form.get("click_delete", None)
            get_start = request.form.get("click_start", None)
            get_execute = request.form.get("click_run", None)
            get_kill_delete = request.form.get("kill_delete", None)
            get_kill_start = request.form.get("kill_start", None)
            get_kill_execute = request.form.get("kill_run", None)
            get_off = request.form.get("off_name", None)
            try:
                if get_off != None:
                    run.killProcess()
            except Exception as e:
                store_error(e)
                return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                       profiles = profiles, schedule_delete_var = schedule_delete_var,
                                       schedule_start_var = schedule_start_var, schedule_execute_var = schedule_execute_var)
            try:
                if get_execute != None:
                    get_time = request.form.get("time_run", None)
                    if get_time == "":
                        store_error("Enter valid time")
                        return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                               profiles = profiles, schedule_delete_var = schedule_delete_var,
                                               schedule_start_var = schedule_start_var,
                                               schedule_execute_var = schedule_execute_var)

                    if get_execute in profiles:
                        schedule_execute_main.kill_value_exe = [0]
                        schedule_execute_var = []
                        time.sleep(1)
                        schedule_execute_var = [get_time]
                        schedule_execute_main.kill_value_exe = [1]
                        threading.Thread(target = schedule_execute_main.call_with_timer_exe, args = (get_time, get_execute)).start()
                        # schedule_execute_main.call_with_timer_exe(get_time, get_execute)
                        store_error("Schedule set for execution at '{}'".format(get_time))
                        return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                           profiles = profiles, schedule_delete_var = schedule_delete_var,
                                           schedule_start_var = schedule_start_var, schedule_execute_var = schedule_execute_var)
                    else:
                        store_error("Profile not found")
                        return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                               profiles = profiles, schedule_delete_var = schedule_delete_var,
                                               schedule_start_var = schedule_start_var,
                                               schedule_execute_var = schedule_execute_var)
            except Exception as e:
                store_error(e)
                return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                       profiles = profiles, schedule_delete_var = schedule_delete_var,
                                       schedule_start_var = schedule_start_var, schedule_execute_var = schedule_execute_var)

            try:
                if get_kill_execute != None:
                    schedule_execute_main.kill_value_exe = [0]
                    schedule_execute_var = []
                    time.sleep(1)
                    return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                           profiles = profiles, schedule_delete_var = schedule_delete_var,
                                           schedule_start_var = schedule_start_var, schedule_execute_var = schedule_execute_var)
            except Exception as e:
                store_error(e)
                return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                       profiles = profiles, schedule_delete_var = schedule_delete_var,
                                       schedule_start_var = schedule_start_var, schedule_execute_var = schedule_execute_var)
            try:
                if get_delete != None:
                    get_time = request.form.get("time_delete", None)
                    if get_time == "":
                        store_error("Enter valid time")
                        return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                               profiles = profiles, schedule_delete_var = schedule_delete_var,
                                               schedule_start_var = schedule_start_var,
                                               schedule_execute_var = schedule_execute_var)
                    schedule_delete_main.kill_value_delete = [0]
                    time.sleep(1)
                    schedule_delete_var = [get_time]
                    schedule_delete_main.kill_value_delete = [1]
                    threading.Thread(target = schedule_delete_main.call_with_timer_delete, args = (get_time, )).start()
                    # schedule_delete_main.call_with_timer_delete(get_time)
                    store_error("Schedule set for delete files at '{}'".format(get_time))
                    return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                           profiles = profiles, schedule_delete_var = schedule_delete_var,
                                           schedule_start_var = schedule_start_var,
                                           schedule_execute_var = schedule_execute_var)
            except Exception as e:
                store_error(e)
                return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                       profiles = profiles, schedule_delete_var = schedule_delete_var,
                                       schedule_start_var = schedule_start_var, schedule_execute_var = schedule_execute_var)
            try:
                if get_kill_delete != None:
                    schedule_delete_main.kill_value_delete = [0]
                    schedule_delete_var = []
                    time.sleep(1)
                    return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                           profiles = profiles, schedule_delete_var = schedule_delete_var,
                                           schedule_start_var = schedule_start_var,
                                           schedule_execute_var = schedule_execute_var)
            except Exception as e:
                store_error(e)
                return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                       profiles = profiles, schedule_delete_var = schedule_delete_var,
                                       schedule_start_var = schedule_start_var, schedule_execute_var = schedule_execute_var)

            try:
                if get_start != None:
                    get_time = request.form.get("time_start", None)
                    if get_time == "":
                        store_error("Enter valid time")
                        return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                               profiles = profiles, schedule_delete_var = schedule_delete_var,
                                               schedule_start_var = schedule_start_var,
                                               schedule_execute_var = schedule_execute_var)
                    schedule_start_main.kill_value_start = [0]
                    time.sleep(1)
                    schedule_start_var = [get_time]
                    schedule_start_main.kill_value_start = [1]
                    threading.Thread(target = schedule_start_main.call_with_timer_start, args = (get_time, )).start()
                    # schedule_delete_main.call_with_timer_start(get_time)
                    store_error("Schedule set for start process at '{}'".format(get_time))
                    return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                           profiles = profiles, schedule_delete_var = schedule_delete_var,
                                           schedule_start_var = schedule_start_var,
                                           schedule_execute_var = schedule_execute_var)
            except Exception as e:
                store_error(e)
                return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                       profiles = profiles, schedule_delete_var = schedule_delete_var,
                                       schedule_start_var = schedule_start_var, schedule_execute_var = schedule_execute_var)
            try:
                if get_kill_start != None:
                    schedule_start_main.kill_value_start = [0]
                    schedule_start_var = []
                    time.sleep(1)
                    return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                           profiles = profiles, schedule_delete_var = schedule_delete_var,
                                           schedule_start_var = schedule_start_var,
                                           schedule_execute_var = schedule_execute_var)
            except Exception as e:
                store_error(e)
                return render_template("index.html", bookmarks_exe = bookmarks_exe, errors = errors,
                                       profiles = profiles, schedule_delete_var = schedule_delete_var,
                                       schedule_start_var = schedule_start_var, schedule_execute_var = schedule_execute_var)


        return render_template("index.html", bookmarks_exe=bookmarks_exe, errors=errors, profiles=profiles, schedule_delete_var=schedule_delete_var,
                               schedule_start_var = schedule_start_var, schedule_execute_var = schedule_execute_var)

except Exception as e:
    store_error(e)
