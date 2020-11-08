import os
import sys
import shutil
import click
from termcolor import colored


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


@click.group()
def cli():
    pass


@cli.command()
@click.option('--path', help="Enter path to save in user_path.txt.")
def setPath(user_path):
    filename = 'user_path.txt'
    if os.path.exists(filename) == True:
        filename = 'user_path.txt'
        path_file = open(filename, "w")
        correct_path = check_path(user_path)
        path_file.write(correct_path)
        path_file.close()


@cli.command()
@click.option('--path', is_flag=True, default=False, is_eager=True, help="Enter path where create new directory.")
@click.argument('value', required=False)
def make_directory(path, value=None):
    if path and value is not None:
        path = value
    else:
        path = get_path()

    path = check_path(path) + '/'
    name = input("Enter dir name: ")

    new_path = os.path.join(path, name)
    click.echo(new_path)
    try:
        os.mkdir(new_path)
        click.echo("Directory create succesfully. Path: {}". format(new_path))
    except OSError as error:
        if error.errno == os.errno.EEXIST:
            click.echo(error)


@cli.command()
@click.option('--path', is_flag=True, default=False, is_eager=True, help="Enter path where is file to rename.")
@click.argument('value', required=False)
def rename_file(path, value=None):
    if path and value is not None:
        path = value+'/'
    else:
        path = get_path()+'/'
    filename = str(
        path+'{}'.format(input("\nEnter filename (with extension): ")))
    click.echo("\nEnter new name (with extension): ")
    try:
        new_filename = str(path+input())
        filename = os.rename(filename, new_filename)
        click.echo("Succesfully renamed.")
        return filename
    except IOError as error:
        click.echo(error)


@cli.command()
@click.option('--path', is_flag=True, default=False, is_eager=True, help="Enter path where show objects.")
@click.argument('value', required=False)
def show_inside(path, value=None):
    if path and value is not None:
        path = value
    else:
        path = get_path()
    click.echo("\nObjects in directory: {}".format(path))
    files = os.scandir(path)
    for element in files:
        if element.is_dir():
            click.echo(colored(element.name, 'blue'))
        else:
            click.echo(element.name)


@cli.command()
@click.option('--path', is_flag=True, default=False, is_eager=True, help="Enter path where delete file.")
@click.argument('value', required=False)
def delete_file(path, value=None):
    if path and value is not None:
        path = value
    else:
        path = get_path()
    chose_file = input("Which file you want to delete? ")
    click.echo(
        "\nAre you sure you want to delete {}? Yes [y] or not [n]". format(chose_file))
    sure = input().lower()

    flag = True
    while flag:
        if sure == 'y':
            try:
                os.remove(chose_file)
                click.echo('{} removed succesfully.' .format(chose_file))
                flag = False
            except OSError as error:
                click.echo(error)
                click.echo('File cannot be removed.')
                flag = False
        elif sure == 'n':
            flag = False
        else:
            ("You have to enter y or n.")
            flag = True
            sure = input().lower()


@cli.command()
@click.option('--path', is_flag=True, default=False, is_eager=True, help="Enter path where delete directory")
@click.argument('value', required=False)
def delete_dir(path, value=None):
    if path and value is not None:
        path = str(value)
    else:
        path = get_path()
    click.echo(is_empty(path))
    click.echo(
        "\nAre you sure you want to delete directory? Yes [y] or not [n]")
    sure = input().lower()
    flag = True
    while flag:
        if sure == 'y':
            try:
                shutil.rmtree(path)
                click.echo('{} removed succesfully' .format(path))
                flag = False
            except OSError as error:
                click.echo(error)
                click.echo('File path cannot be removed.')
                flag = False
        elif sure == 'n':
            flag = False
        else:
            ("You have to enter y or n.")
            flag = True
            sure = input().lower()


if __name__ == '__main__':
    cli()
