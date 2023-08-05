"""Module for iterating through and printing any number of nested lists, Chapter 1 of Head First Python"""

import sys

def print_lol(the_list, indent=False, level=0, fh=sys.stdout):
        for each_item in the_list:
                """The function is recursive, if the current element is a list then
                the function recurrs - otherwise, if indent is true, it prints level
                number of tabs and then the item. The output place is specified by
                the parameter file."""
                if isinstance(each_item, list):
                        print_lol(each_item, indent, level+1, fh)
                else:
                        if indent:
                                for level_num in range(level):
                                        print("\t", end='', file=fh)
                        print(each_item, file=fh)
