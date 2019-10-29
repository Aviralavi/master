import os
import time
import sys
from flaskpackage.routes.route_delete import errors

batch_cmd = []
pass_fail = []
cwd = []
get_id = []
current_time = []
kill_value_exe_main = [1]

def store_error(error):
    errors.append(error)

def find_log(cd_value, new_sorted_files):
    try:
        file_path = os.path.join(cd_value, new_sorted_files[0])
        # current_time = time.strftime('%Y/%m/%d/%H%M', time.localtime())
        modificationTime = time.strftime('%Y/%m/%d/%H%M', time.localtime(os.path.getmtime(file_path)))

        if current_time[-1] == modificationTime:
            f = open(file_path, encoding="utf8")
            for line in reversed(list(f)):
                if line.startswith('window.output["stats"]'):
                    line = line.split("}],")
                    line = line[0].strip()
                    if '"fail":0,"label":"All Tests"' in line:
                        pass_fail.append({get_id[-1]:"PASS"})
                        store_error("PASS log: {}".format(file_path))
                        break
                    else:
                        pass_fail.append({get_id[-1]:"FAIL"})
                        store_error("FAIL log: {}".format(file_path))
            f.close()
        else:
            pass_fail.append({get_id[-1]: "ERROR"})
            store_error("logs not found")
    except Exception as e:
        pass_fail.append({get_id[-1]:"ERROR"})
    finally:
        os.chdir(cwd[-1])


def get_allfiles(dir_file):
    try:
        new_sorted_files = []
        os.chdir(dir_file)
        sorted_files = sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime)
        for files in sorted_files:
            if files.endswith(".html") or files.endswith(".htm"):
                new_sorted_files.append(files)
    except Exception as e:
        store_error('Provide "CD %workspace%" in command for logs verification')
    return new_sorted_files


def get_directory_location(batch_command):
    f = open(batch_command, "r")
    if f.mode == 'r':
        contents = f.read()
        cd_file = contents.split('\n')
        f.close()
        for files in cd_file:
            if files.strip().startswith('CD'):
                files = files.strip()[3:]
                files = files.strip()
                break
    return files


def multiCMD(batch_command):
    cmd_string = "start /wait cmd /c {}".format(batch_command)
    os.system(cmd_string)
    global current_time
    current_time = []
    current_time.append(time.strftime('%Y/%m/%d/%H%M', time.localtime()))

def get_commands(file_input):
    global kill_value_exe_main
    if kill_value_exe_main[-1] != 0:
        file_input = file_input[0].strip()
        cwd.append(os.getcwd())
        write_var = "temp.bat".format(file_input)
        fileWrite = open(write_var, "w+")
        fileWrite.write(file_input)
        fileWrite.close()
        batch_cmd.append(write_var)
        multiCMD(write_var)
        # try:
        #     os.chdir(cwd)
            # os.remove(write_var)
        # except Exception as e:
        #     print(e)
    else:
        kill_value_exe_main = [1]
        store_error("Execution stopped")
        sys.exit()

def get_log_output():
    cd_value = get_directory_location(batch_cmd[-1])
    new_sorted_files = get_allfiles(cd_value)
    if not new_sorted_files:
        store_error("logs not found")
    find_log(cd_value, new_sorted_files)

# get_log_output()

# def get_commands_input_files(file_input):
#     cwd = os.getcwd()
#     file_input = "C:\\deletefile\\New folder\\test.txt"
#     f = open(file_input, "r")
#     if f.mode == 'r':
#         contents = f.read()
#         list_commands = contents.split('\n\n')
#         index = int(0)  # type: int
#         for files in list_commands:
#             index = index + 1
#             write_var = "temp{}.bat".format(index)
#             fileWrite = open(write_var, "w+")
#             fileWrite.write(files)
#             fileWrite.close()
#             print(files)
#             multiCMD(write_var)
#             try:
#                 os.chdir(cwd)
#                 os.remove(write_var)
#             except Exception as e:
#                 print(e)

