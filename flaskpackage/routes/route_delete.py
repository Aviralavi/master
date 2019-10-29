from flask import render_template, url_for, request, redirect
from flaskpackage import deleteMain, model, app, db

bookmarks_del = []

def store_bookmark_del():
    global bookmarks_del
    bookmarks_del = []
    getAllData = model.DeleteTable.query.all()
    alldateLength = len(getAllData)
    for datarange in range(0, alldateLength):
        getAllDataString = str(getAllData[datarange])
        containAlldataDict = getAllDataString.split(":::")
        bookmarks_del.append(dict({containAlldataDict[0]: containAlldataDict[1]}))

global errors
errors = []

def store_error(error):
    errors.append(error)

class User:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def initials(self):
        return "{} {}".format(self.firstname, self.lastname)




# @app.route('/add_url.html', methods=['GET', 'POST'])
# def add_url_method():
#     return render_template("add_url.html")


try:
    @app.route('/delete', methods=['GET', 'POST'])
    def delete():
        global redirect_html
        redirect_html = 'delete.html'
        if request.method == "POST":
            getBookmarkLength = len(bookmarks_del)
            get_add = request.form.get("addName", None)
            get_file = request.form.get("add_file", None)
            get_deleteClicked = request.form.get("deleteClicked", None)
            get_off_delete = request.form.get("off2_name", None)

            if get_off_delete != None:
                deleteMain.kill_value_delete_main = [0]
                store_error("Stopping delete process")
                return render_template(redirect_html, bookmarks_del = bookmarks_del, errors = errors)

            if get_deleteClicked != None:
                store_bookmark_del()
                try:
                    deleteMain.kill_value_delete_main = [1]
                    count = 1
                    for delete_main_pass in bookmarks_del:
                        for get_key, get_val in delete_main_pass.items():
                            checkval = "check" + str(count)
                            count += 1
                            get_check = request.form.get(checkval, "off")
                            if get_check != "off":
                                try:
                                    deleteMain.deleteFiles(get_val)
                                    store_error("'{}\*' deleted successfully".format(get_val))
                                except Exception as e:
                                    store_error(e)
                except Exception as e:
                    store_error(e)
                    return render_template("delete.html", bookmarks_del=bookmarks_del, errors=errors)

            if get_add != None:
                try:
                    redirect_html = "add_url.html"
                    store_bookmark_del()
                    return render_template("add_url.html", bookmarks_del=bookmarks_del, errors=errors)
                except Exception as e:
                    store_error(e)
                    return render_template("add_url.html", bookmarks_del=bookmarks_del, errors=errors)

            if get_file != None:
                try:
                    redirect_html = "delete.html"
                    get_name = request.form.get("name_add", None)
                    get_url = request.form.get("url_add", None)
                    if get_name != "":
                        if get_url == "C:\\" or get_url == "D:\\" or get_url == "E:\\" or get_url == "F:\\" \
                                or get_url == "G:\\" or get_url == "H:\\" or get_url == "I:\\" or get_url == "J:\\":
                            redirect_html = "add_url.html"
                            store_error("Adding '{}' not allowed".format(get_url))
                            store_bookmark_del()
                            return render_template("add_url.html", bookmarks_del=bookmarks_del, errors=errors)

                        elif get_name != "" and get_url != "":
                            storeDelValue = model.DeleteTable(name=get_name, path=get_url)
                            db.session.add(storeDelValue)
                            db.session.commit()
                            store_error("{} added successfully".format(get_name))
                            store_bookmark_del()
                            return render_template("delete.html", bookmarks_del=bookmarks_del, errors=errors)
                        else:
                            redirect_html = "add_url.html"
                            store_error("Enter valid name and path")
                            store_bookmark_del()
                            return render_template("add_url.html", bookmarks_del=bookmarks_del, errors=errors)
                except Exception as e:
                    store_error(e)
                    return render_template("add_url.html", bookmarks_del=bookmarks_del, errors=errors)

            for deleteCount in range(getBookmarkLength):
                try:
                    deleteIMGval = "deleteIMGval" + str(deleteCount + 1)
                    get_delete_logo = request.form.get(deleteIMGval, None)
                    if get_delete_logo != None:
                        get_name = "name" + get_delete_logo
                        get_name = request.form.get(get_name, None)
                        execute_sql = "DELETE FROM delete_table WHERE name = '{}';".format(get_name)
                        db.engine.execute(execute_sql)
                        store_error("{} removed successfully".format(get_name))
                        redirect_html = "delete.html"
                        store_bookmark_del()
                        return render_template("delete.html", bookmarks_del=bookmarks_del, errors=errors)
                except Exception as e:
                    store_error(e)
                    return render_template("delete.html", bookmarks_del=bookmarks_del, errors=errors)

            # if get_url.startswith("http"):
            #     error = "error in url"
            #     store_error(error)
            #     return render_template('index.html', errors=str(errors[len(errors) - 1]),
            #                            title="Title passed from view to template",
            #                            user=User("aviral", "verma"))

        # app.logger.debug('stored url: ' + "url")
        # flash("stored {}".format(get_url))
        # return redirect(url_for('delete'))
        store_bookmark_del()
        return render_template(redirect_html, bookmarks_del=bookmarks_del, errors=errors)
except Exception as e:
    store_error(e)

