import os
import sys
import shutil
import click
import subprocess
from termcolor import colored


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
@click.option('--make', is_flag=True, default=False, is_eager=True, help="Enter path where create new directory.")
@click.option('--delete', is_flag=True, default=False, is_eager=True, help="Enter path where delete directory.")
@click.option('--rename', is_flag=True, default=False, is_eager=True, help="Enter path where delete directory.")
@click.option('--smod', is_flag=True, default=False, is_eager=True, help="Enter path to show directory permission.")
@click.option('--chmod', is_flag=True, default=False, is_eager=True, help="Enter path to change directory permission.")
@click.option('--move', is_flag=True, default=False, is_eager=True, help="Enter path where directory is.")

@click.argument('value', required=False)
def directory(move,smod, chmod, make, delete, rename, value=None):
    if value:
        value = check_path(value)

    if make:
        if value is not None:
            make = value
        else:
            make = get_path()

        make = check_path(make) + '/'
        name = input("Enter dir name: ")

        new_path = os.path.join(make, name)
        click.echo(new_path)
        try:
            os.mkdir(new_path)
            click.echo(
                "Directory create succesfully. Path: {}". format(new_path))
        except OSError as error:
            if error.errno == os.errno.EEXIST:
                click.echo(error)

    elif move:
        if value is not None:
            move = value
        else:
            move = get_path()

        new_path = input("Enter path destination: ")
        new_path = check_path(new_path)
        try:
            shutil.move(move, new_path)
            print("OK")
        except IOError as error:
            click.echo(error)

    elif chmod:
        if value is not None:
            chmod = value
        else:
            chmod = get_path()

        mode = input("Enter mode: (like 777) ")
        try:
            subprocess.call(['chmod', '0' + mode, chmod])
            click.echo("Directory permission code: {}".format(mode))
        except IOError as error:
            click.echo(error)

    elif smod:

        if value is not None:
            smod = value
        else:
            smod = get_path()

        try:
            stats = os.stat(smod)
            click.echo("Directory permission: {}".format(oct(stats.st_mode)))
        except IOError as error:
            click.echo(error)

    elif delete:
        selete = check_path(delete)
        if value is not None:
            delete = str(value)
        else:
            delete = get_path()
        click.echo(is_empty(delete))
        click.echo(
            "\nAre you sure you want to delete directory? Yes [y] or not [n]")
        sure = input().lower()
        flag = True
        while flag:
            if sure == 'y':
                try:
                    shutil.rmtree(delete)
                    click.echo('{} removed succesfully' .format(delete))
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

    else:
        print_help()


@cli.command()
@click.option('--delete', is_flag=True, default=False, is_eager=True, help="Enter path where delete file.")
@click.option('--make', is_flag=True, default=False, is_eager=True, help="Enter path where make file.")
@click.option('--rename', is_flag=True, default=False, is_eager=True, help="Enter path where is file to rename.")
@click.option('--smod', is_flag=True, default=False, is_eager=True, help="Enter path to show file mode.")
@click.option('--chmod', is_flag=True, default=False, is_eager=True, help="Enter path to change file permission.")
@click.option('--move', is_flag=True, default=False, is_eager=True, help="Enter path where file is.")
@click.argument('value', required=False)
def file(move, smod, chmod, make, delete, rename, value=None):
    if value:
        value = check_path(value)

    if make:
        if value is not None:
            make = value
            print("in if: ", make)
        else:
            make = get_path()

        filename = input("Enter filename (with extension): ")
        try:
            path = os.path.join(make, filename)
            click.echo(path)
            new_file = os.mknod(path)
        except IOError as error:
            raise error

    elif move:
        if value is not None:
            move = value + '/'
        else:
            move = get_path() + '/'

        chose_file = input("Enter filename (with extension): ")
        enter = move+chose_file
        new_path = input("Enter path destination: ")
        new_path = check_path(new_path)
        new_path = new_path + '/' + chose_file
        try:
            shutil.move(enter, new_path)
            print("OK")
        except IOError as error:
            click.echo(error)

    elif chmod:
        if value is not None:
            chmod = value + '/'
        else:
            chmod = get_path() + '/'

        chose_file = input("Enter filename (with extension): ")
        enter = chmod+chose_file
        mode = input("Enter mode: (like 777) ")
        try:
            subprocess.call(['chmod', '0' + mode, enter])
            click.echo("File permission code: {}".format(mode))
        except IOError as error:
            click.echo(error)

    elif smod:
        if value is not None:
            smod = value + '/'
        else:
            smod = get_path() + '/'
        chose_file = input("Enter filename (with extension): ")

        stats1 = smod + chose_file
        stats = os.stat(stats1)
        print("File permission: ", oct(stats.st_mode))

    elif delete:
        if value is not None:
            delete = value
        else:
            delete = get_path()
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

    elif rename:
        if value is not None:
            rename = value+'/'
        else:
            rename = get_path()+'/'
        filename = str(
            rename+'{}'.format(input("\nEnter filename (with extension): ")))
        click.echo("\nEnter new name (with extension): ")
        try:
            new_filename = str(rename+input())
            filename = os.rename(filename, new_filename)
            click.echo("Succesfully renamed.")
            return filename
        except IOError as error:
            click.echo(error)
    else:
        print_help()


if __name__ == '__main__':
    cli()
