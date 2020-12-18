import click
import os
from sys import platform
import sys


def check_so():
    if platform == "linux" or platform == "linux2":
        return True
    else:
        return False


def print_help():
    help = click.get_current_context()
    click.echo(help.get_help())
    help.exit()


def check_path(path):
    isExist = os.path.exists(path)
    flag = True
    while flag:
        isExist = os.path.exists(path)
        if not isExist:
            path = input("Invalid path. Enter correct path.\n")
            flag = True
        else:
            click.echo("\nValid path.")
            flag = False
            click.echo("\nCurrent Path: {}".format(path))
            return path


def is_empty(path):
    files = os.listdir(path)
    count = 0
    pl = ''
    for element in files:
        count += 1
    if count not in {0, 1}:
        pl = 'are'
    else:
        pl = 'is'
    return "There {} {} objects in directory.".format(pl, count)


def get_path():
    filename = "user_path.txt"
    with open(filename, "r") as myFile:
        if os.stat(filename).st_size == 0:
            click.echo("{} is empty.".format(filename))
            path = check_path("")
            return path
        else:
            newFile = myFile.read().rstrip()
            return newFile


def set_path(path):
    if path:
        filename = 'user_path.txt'
        if os.path.exists(filename) == True:
            filename = 'user_path.txt'
            path_file = open(filename, "w")
            correct_path = check_path(path)
            path_file.write(correct_path)
            path_file.close()
            return correct_path
        else:
            return False
