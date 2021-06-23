import os

def greetings():

    print("\n-------------------------------")
    print("<<<< WELCOME TO PY PDF BOT >>>>")
    print("-------------------------------\n")

def decrease_level(paths):
    
    print("\nDecreasing heading levels by 2 in metric markdowns")

    for i in paths:
        if '/' in i:
            cmd = 'sed -i "s/^\#/###/g" ' + i
            os.system(cmd)

def generate_WG_md(name, level, paths):

    stuff = '#'*level + ' ' + name.upper() + '\n\n' + get_lorem_ipsum()
    name += '.md'

    print("Generating file", name)
    with open(name, 'w') as f:
        f.write(stuff)

    paths.append(name)
    return paths

def get_lorem_ipsum():
    return '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''

