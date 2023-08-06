""" This is the nester module which will help you to print your lists"""

def print_lol(the_list):
    """ The module takes a list and print all the items inside it, no matter
    if there are other lists inside it"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
