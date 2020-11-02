import os
import sys
import shutil
import click
from termcolor import colored

#--show, --delete, --rename, --change, ---exit


def start_path():
    path = input("\nEnter path: ")
    new_path = check_path(path)
    return new_path

def check_path(path):
    isExist = os.path.exists(path)
    flag = True
    while flag:
        isExist = os.path.exists(path)
        if not isExist:
            path = input("\nInvalid path. Enter correct path.")
            flag = True
        else:
            print("\nValid path.")
            flag = False
            print("\nCurrent Path: %s" % path)
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

@click.command()
@click.option('--rename', help = "Rename file")
def rename_file(rename):
    rename = rename+'/'
    filename = str(
        rename+'{}'.format(input("\nEnter filename (with extension): ")))
    print("\nEnter new name (with extension): ")
    try:
        new_filename = str(rename+input())
        filename = os.rename(filename, new_filename)
        print("Succesfully renamed.")
        return filename
    except IOError as error:
        print(error)

@click.command()
@click.option('--show', help = "Show objects in directory")
def show_inside(show):
    click.echo("\nObjects in directory: ")
    files = os.scandir(show)
    for element in files:
        if element.is_dir():
            click.echo(colored(element.name,'blue'))
        else:
            click.echo(element.name)


@click.command()
@click.option('--delete', help = "Delete directory")
def delete_dir(delete):
    click.echo(is_empty(delete))
    click.echo("\nAre you sure you want to delete directory? Yes [y] or not [n]")
    sure = input().lower()
    flag = True
    while flag:
        if sure == 'y':
            try:
                shutil.rmtree(delete)
                click.echo('%s removed succesfully' % delete)
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


@click.command()
@click.option('--exit', help = "Exit program")
def exit_app(exit):
    click.echo("See you next time.")
    sys.exit()

if __name__=='__main__':
    #user_path = start_path()
    show_inside()
    #delete_dir()
    #exit_app()
    rename_file()