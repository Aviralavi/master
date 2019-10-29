import os
import subprocess

from flask import render_template

from flaskpackage import app

pidID = [os.getpid()]
errors = []


def store_error(error):
    errors.append(error)


@app.errorhandler(404)
def pageNotFount(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def pageNotFount(e):
    return render_template('404.html'), 500

# from selenium import webdriver
#
# driver = webdriver.Chrome()
if __name__ == "__main__":
    try:
        # webbrowser.open("https://localhost:9000", new=0, autoraise=True)
        x = app.run(debug=True, host='localhost', port=9000)
    except Exception as e:
        store_error(e)


def killProcess():
    pid = pidID[-1]
    subprocess.Popen('taskkill /F /PID {0}'.format(pid), shell=True)
