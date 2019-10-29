import os
import sys
import flaskpackage.routes.route_delete

kill_value_delete_main = [1]

def store_error(error):
    flaskpackage.routes.route_delete.errors.append(error)

def deleteFiles(folder):
    global kill_value_delete_main
    if kill_value_delete_main[-1] != 0:
        if os.path.isfile(folder):
            os.unlink(folder)
        else:
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    else:
                        os.system('rmdir /S /Q "{}"'.format(file_path))
                except Exception as e:
                    print(e)
    else:
        kill_value_delete_main = [1]
        store_error("Process stopped")
        sys.exit()
