""" This nester.py module includes one function print_lol() which prints lists that may or may not be nested"""

def print_lol(the_list):
        """ This recursive function takes input as the_list(any python list) and prints all the items in the list/nested lists"""
        for each_item in the_list:
                if isinstance(each_item,list):
                        print_lol(each_item)
                else:
                        print(each_item)
