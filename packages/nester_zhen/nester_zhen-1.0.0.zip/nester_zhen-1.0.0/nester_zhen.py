"""This is "nester.py"module, which provide function print_lol,
it can print the list, which may include nested list."""

def print_lol(the_list):
    """The list's item will be print recursionly"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
