import click
import os


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
            path = input("\nInvalid path. Enter correct path.")
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
            raise Exception("{} is empty.".format(filename))
        else:
            newFile = myFile.read().rstrip()
            return(newFile)
