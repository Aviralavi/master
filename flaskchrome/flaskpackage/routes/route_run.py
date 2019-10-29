from flask import render_template, url_for, request, redirect
from flaskpackage import run_process_main, model, app, db
from flaskpackage.routes.route_delete import errors
import os


bookmarks_start = []

def store_bookmark_start():
    global bookmarks_start
    bookmarks_start = []
    getAllData = model.StartTable.query.all()
    alldateLength = len(getAllData)
    for datarange in range(0, alldateLength):
        getAllDataString = str(getAllData[datarange])
        containAlldataDict = getAllDataString.split(":::")
        bookmarks_start.append(dict({containAlldataDict[0]: [containAlldataDict[1], containAlldataDict[2]]}))
        # bookmarks_start.append(dict({containAlldataDict[0]: list(map(lambda x: x, containAlldataDict[1:]))}))

def store_error(error):
    errors.append(error)


try:
    @app.route('/run_process', methods=['GET', 'POST'])
    def run_process():
        global redirect_html
        redirect_html = 'run_process.html'
        if request.method == "POST":
            getBookmarkLength = len(bookmarks_start)
            get_add = request.form.get("addName", None)
            get_file = request.form.get("add_file", None)
            get_run_Clicked = request.form.get("deleteClicked", None)
            get_off_run = request.form.get("off1_name", None)

            if get_off_run != None:
                run_process_main.kill_value_start_main = [0]
                store_error("Stopping process")
                return render_template(redirect_html, bookmarks_start = bookmarks_start, errors = errors)
            if get_run_Clicked != None:
                store_bookmark_start()
                try:
                    run_process_main.kill_value_start_main = [1]
                    count = 1
                    for delete_main_pass in bookmarks_start:
                        for get_key, get_val in delete_main_pass.items():
                            checkval = "check" + str(count)
                            count += 1
                            get_check = request.form.get(checkval, "off")
                            if get_check != "off":
                                try:
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
                                    return render_template("run_process.html", bookmarks_start=bookmarks_start,
                                                           errors=errors)

                except Exception as e:
                    store_error(e)
                    return render_template("run_process.html", bookmarks_start=bookmarks_start, errors=errors)

            if get_add != None:
                try:
                    redirect_html = "run_process_add_url.html"
                    store_bookmark_start()
                    return render_template("run_process_add_url.html", bookmarks_start=bookmarks_start, errors=errors)
                except Exception as e:
                    store_error(e)
                    return render_template("run_process_add_url.html", bookmarks_start=bookmarks_start, errors=errors)

            if get_file != None:
                try:
                    redirect_html = "run_process.html"
                    get_name = request.form.get("name_add", None)
                    get_url = request.form.get("url_add", None)
                    get_repeat = request.form.get("repeat_add", None)
                    if get_name != "" and get_url != "":
                        storeDelValue = model.StartTable(name=get_name, path=get_url, repeat=get_repeat)
                        db.session.add(storeDelValue)
                        db.session.commit()
                        store_error("{} added successfully".format(get_name))
                        store_bookmark_start()
                        print(bookmarks_start)
                        return render_template("run_process.html", bookmarks_start=bookmarks_start, errors=errors)
                    else:
                        redirect_html = "run_process_add_url.html"
                        store_error("Enter valid name and path")
                        store_bookmark_start()
                        return render_template("run_process_add_url.html", bookmarks_start=bookmarks_start, errors=errors)
                except Exception as e:
                    store_error(e)
                    return render_template("run_process_add_url.html", bookmarks_start=bookmarks_start, errors=errors)

            for deleteCount in range(getBookmarkLength):
                try:
                    deleteIMGval = "deleteIMGval" + str(deleteCount + 1)
                    get_delete_logo = request.form.get(deleteIMGval, None)
                    if get_delete_logo != None:

                        get_name = "name" + get_delete_logo
                        get_name = request.form.get(get_name, None)
                        execute_sql = "DELETE FROM start_table WHERE name = '{}';".format(get_name)
                        db.engine.execute(execute_sql)
                        store_error("{} removed successfully".format(get_name))
                        return redirect(url_for('run_process'))
                except Exception as e:
                    redirect_html = "run_process.html"
                    store_error(e)
                    return render_template("run_process.html", bookmarks_start=bookmarks_start, errors=errors)

        store_bookmark_start()
        return render_template(redirect_html, bookmarks_start=bookmarks_start, errors=errors)
except Exception as e:
    store_error(e)
