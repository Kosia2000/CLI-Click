import click
import os
import re
import shutil
import subprocess
import sys
from helpers import *
from termcolor import colored


@click.group()
def cli():
    pass


@cli.command()
def getPath():
    path = get_path()
    click.echo("Current path is {}".format(path))


@cli.command()
@click.option('--path', help="Enter path to save in user_path.txt.")
def setPath(path):
    if not set_path(path):
        print_help()


@cli.command()
@click.option('--show', is_flag=True, default=False, is_eager=True, help="Enter path where show what is inside.")
@click.option('--make', is_flag=True, default=False, is_eager=True, help="Enter path where create new directory.")
@click.option('--delete', is_flag=True, default=False, is_eager=True, help="Enter path where delete directory.")
@click.option('--rename', is_flag=True, default=False, is_eager=True, help="Enter path where is the directory.")
@click.option('--smod', is_flag=True, default=False, is_eager=True, help="Enter path to show directory permission.")
@click.option('--chmod', is_flag=True, default=False, is_eager=True, help="Enter path to change directory permission.")
@click.option('--move', is_flag=True, default=False, is_eager=True, help="Enter path where directory is.")
@click.argument('value', required=False)
def directory(show, move, smod, chmod, make, delete, rename, value=None):
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
    elif show:
        if value is not None:
            show = value
        else:
            show = get_path()

        files = os.scandir(show)
        for element in files:
            if element.is_dir():
                click.echo(colored(element.name, 'blue'))
            elif element.is_file():
                click.echo(colored(element.name, 'green'))
            else:
                click.echo(element.name)

    elif move:
        if value is not None:
            move = value
        else:
            move = get_path()

        click.echo("Moving {}".format(move))
        new_path = input("Enter path destination: ")
        new_path = check_path(new_path)
        try:
            shutil.move(move, new_path)
        except IOError as error:
            click.echo(error)

    elif chmod:
        if value is not None:
            chmod = value
        else:
            chmod = get_path()

        click.echo("Change a mode of {}".format(chmod))
        mode = ""
        returncode = -1

        while not re.match("[0-7]{3}", mode) and returncode != 0:
            mode = input("Enter mode: (like 777) ")
            returncode = subprocess.call(['chmod', '0' + mode, chmod])
            click.echo("Directory permission code: {}".format(mode))

    elif smod:
        if value is not None:
            smod = value
        else:
            smod = get_path()

        try:
            stats = os.stat(smod)
            click.echo("Directory permission: {}".format(
                str(oct(stats.st_mode)[-3:])))
        except IOError as error:
            click.echo(error)

    elif delete:
        if value is not None:
            delete = check_path(str(value))
        else:
            delete = get_path()

        click.echo(is_empty(delete))
        click.echo(
            "\nAre you sure you want to delete directory: {}? Yes [y] or not [n]".format(delete))
        sure = input().lower()
        flag = True
        while flag:
            if sure == 'y':
                try:
                    shutil.rmtree(delete)
                    click.echo('{} removed succesfully'.format(delete))
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

    elif rename:
        if value is not None:
            rename = check_path(value)
        else:
            rename = get_path()

        split_rename = rename.split("/")
        old_name = split_rename[:-1]
        shorter_path = str("/".join(old_name)+"/")

        new_name = input("Enter new directory name\n")
        new_path = shorter_path + new_name
        try:
            changing = os.rename(rename, new_path)
            click.echo(new_path)
        except Exception as ex:
            click.echo(ex)

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
            click.echo("in if: ", make)
        else:
            make = get_path()

        filename = input("Enter filename (with extension): ")
        try:
            path = os.path.join(make, filename)
            click.echo(path)
            new_file = os.mknod(path)
            click.echo("Created file: {}".format(filename))
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
            click.echo("File moved successfully")
        except IOError as error:
            click.echo(error)

    elif chmod:
        if value is not None:
            chmod = value + '/'
        else:
            chmod = get_path() + '/'

        chose_file = input("Enter filename (with extension):\n ")
        click.echo("Change a mode of {}".format(chose_file))
        mode = ""
        returncode = -1

        enter = chmod+chose_file

        while not re.match("[0-7]{3}", mode) and returncode != 0:
            mode = input("Enter mode: (like 777) ")
            returncode = subprocess.call(['chmod', '0' + mode, enter])
            click.echo("File permission code: {}".format(mode))

    elif smod:
        if value is not None:
            smod = value + '/'
        else:
            smod = get_path() + '/'
        chose_file = input("Enter filename (with extension): ")

        stats1 = smod + chose_file
        try:
            stats = os.stat(stats1)
            click.echo("File permission: {}".format(
                str(oct(stats.st_mode)[-3:])))
        except Exception as ex:
            click.echo(ex)

    elif delete:
        if value is not None:
            delete = value+'/'
        else:
            delete = get_path()+'/'
        chose_file = input("Which file you want to delete? ")
        click.echo(
            "\nAre you sure you want to delete {}? Yes [y] or not [n]". format(chose_file))
        sure = input().lower()
        delete_path = delete + chose_file
        flag = True
        while flag:
            if sure == 'y':
                try:
                    os.remove(delete_path)
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
            rename+'{}'.format(input("\nEnter filename to change (with extension): \n")))
        click.echo("\nEnter new name (with extension): \n")
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
    if check_so():
        cli()
    else:
        click.echo("Use the linux as the requirements file says so.")
        sys.exit(-1)
