import os
import sys
import shutil
import click
from termcolor import colored

#--show, --delete, --rename, --change, ---exit, --make_dir


# DONE
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

# DONE
@click.command()
@click.option('--my_path', help="Enter path")
def setPath(my_path):
    filename = 'user_path.txt'
    if os.path.exists(filename) == True:
        filename = 'user_path.txt'
        path_file = open(filename, "w")
        correct_path = check_path(my_path)
        path_file.write(correct_path)
        path_file.close()

# DONE
def get_path():
    with open("user_path.txt", "r") as myFile:
        newFile = myFile.read().rstrip()
    return(newFile)

# DONE
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

# DONE
@click.command()
@click.option('--make_dir', is_flag=True, default=False, is_eager=True, help="Make new directory")
@click.argument('value', required=False)
def make_directory(make_dir, value = None):
    if make_dir and value is not None:
        make_dir = value
    else:
        make_dir = get_path()
    
    make_dir = check_path(make_dir) + '/'
    name = input("Enter dir name: ")

    new_path = os.path.join(make_dir, name)
    click.echo(new_path)
    try:
        os.mkdir(new_path)
        click.echo("Directory create succesfully. Path: {}". format(new_path))
    except OSError as error:
        if error.errno == os.errno.EEXIST:
            click.echo(error)  

# DONE
@click.command()
@click.option('--rename', is_flag=True, default=False, is_eager=True, help="Rename file")
@click.argument('value', required=False)
def rename_file(rename, value=None):
    if rename and value is not None:
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

# DONE
@click.command()
@click.option('--show', is_flag=True, default=False, is_eager=True, help="Show objects in directory")
@click.argument('value', required=False)
def show_inside(show, value=None):
    if show and value is not None:
        show = value
    else:
        show = get_path()
    click.echo("\nObjects in directory: {}".format(show))
    files = os.scandir(show)
    for element in files:
        if element.is_dir():
            click.echo(colored(element.name, 'blue'))
        else:
            click.echo(element.name)



# DONE
@click.command()
@click.option('--del_file', is_flag=True, default=False, is_eager=True, help="Delete file in directory")
@click.argument('value', required=False)
def delete_file(del_file, value = None):
    if del_file and value is not None:
        del_file = value
    else:
        del_file = get_path()
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
    



# DONE
@click.command()
@click.option('--delete', is_flag=True, default=False, is_eager=True, help="Delete directory")
@click.argument('value', required=False)
def delete_dir(delete, value=None):
    if delete and value is not None:
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

# DONE
@click.command()
@click.option('--exit', is_flag=True, help="Exit program")
def exit_app(exit):
    click.echo("See you next time.")
    sys.exit()


#if __name__ == '__main__':
setPath()
    #user_path = start_path()
show_inside()
    #delete_dir()
    # exit_app()
    # rename_file()
    #make_directory()
delete_file()