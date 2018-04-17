import sys
import os
from os.path import isfile, isdir, join
from subprocess import call

page_data = "page_data"
current_dir = "adrian83.github.io"
files = [".git", "data", "page_data", "dev.py", "index.html", "README.md"]

def _remove(elem_path):
    if isfile(elem_path):
        os.remove(elem_path)
    if isdir(elem_path):
        for elem in os.listdir(elem_path):
            _remove(join(elem_path, elem))
        os.rmdir(elem_path)

def clean():
    cwd = os.getcwd()
    if not cwd.endswith(current_dir):
        print("Script can only be executed in '{0}' directory".format(current_dir))
        return
    to_remove = [f for f in os.listdir(cwd) if f not in files] #isfile(join(mypath, f))]
    print("files / directories {0} will be removed".format([join(cwd, e) for e in to_remove]))
    for elem in to_remove:
        _remove(elem)

def build():
    cwd = os.getcwd()
    os.chdir(join(cwd, page_data))
    call("hugo")
    os.chdir(cwd)



def printMenu():
    print("\n")
    print("----- MENU -----")
    print("menu   - prints menu")
    print("clean  - removes all old files")
    print("build  - builds new version")
    print("deploy - deploys new version ")
    print("all    - cleans old version, builds and deploys new one, pushes everything to github")
    print("\n")




if len(sys.argv) < 2:
    printMenu()

if sys.argv[1] == "menu":
    printMenu()

if sys.argv[1] == "clean":
    clean()

if sys.argv[1] == "build":
    build()
