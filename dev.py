import sys
import os
from os.path import isfile, isdir, join
from subprocess import call
import shutil


page_data = "page_data"
public = join(page_data, "public")
current_dir = "adrian83.github.io"
files = [".git", "data", page_data, "dev.py", "README.md", ".gitignore", ".gitmodules", ".nojekyll"]

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
        _remove(join(cwd, elem))

def build():
    cwd = os.getcwd()
    os.chdir(join(cwd, page_data))
    call("hugo")
    os.chdir(cwd)

def deploy():
    cwd = os.getcwd()
    public_path = join(cwd, public)
    for item in os.listdir(public_path):
        item_path = join(public_path, item)
        if isdir(item_path):
            shutil.copytree(item_path, join(cwd, item))
        elif isfile(item_path):
            shutil.copyfile(item_path, join(cwd, item))

def all():
    clean()
    build()
    deploy()

def printMenu():
    print("\n")
    print("----- MENU -----")
    print("menu   - prints menu")
    print("clean  - removes all old files")
    print("build  - builds new version")
    print("deploy - deploys new version ")
    print("all    - cleans old version, builds and deploys new one")
    print("\n")






if len(sys.argv) < 2:
    printMenu()
elif sys.argv[1] == "menu":
    printMenu()
elif sys.argv[1] == "clean":
    clean()
elif sys.argv[1] == "build":
    build()
elif sys.argv[1] == "deploy":
    deploy()
elif sys.argv[1] == "all":
    all()