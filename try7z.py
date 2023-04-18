import os
import re 
import subprocess

from tkinter import filedialog
from tkinter import messagebox
from tkinter import Tk

root = Tk()
root.withdraw()

PASSWORD_FILE="passwords.txt"

def input_zip_file():
    file_path = filedialog.askopenfilename()
    return file_path

def get_password_list():
    if not os.path.exists(PASSWORD_FILE):
        return []
    with open(PASSWORD_FILE) as file:
        lines = [line.rstrip() for line in file]
    return lines

def search_password(zip_file, password_list):
    for p in password_list:
        print('Try password: {}'.format(p))
        result = str(subprocess.run(['7z', '-y', 't', zip_file, '-p{{{}}}'.format(p)], stdout=subprocess.PIPE))
        if re.match(r'.*Everything is Ok', result) is not None:
            return p

def main():
    zip_file = input_zip_file()
    if not os.path.exists(zip_file):
        messagebox.showinfo("Warning", "File does not exist")
        exit()

    password_list = get_password_list()
    if len(password_list) == 0:
        messagebox.showinfo("Warning", "Password file is empty")
        exit()

    password = search_password(zip_file, password_list)
    if password is not None:
        print("Password is: {}".format(password))
        messagebox.showinfo("Completed", "Password is: {}".format(password))
    else:
        messagebox.showinfo("Warning", "Failed to search password")

main()