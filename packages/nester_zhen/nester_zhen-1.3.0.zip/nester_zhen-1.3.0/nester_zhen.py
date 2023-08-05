"""This is "nester.py"module, which provide function print_lol,
it can print the list, which may include nested list."""
from __future__ import print_function

def print_lol(the_list,indent=False,level=0):
    """The list's item will be print recursionly"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print ("\t",end='')
            print(each_item)
