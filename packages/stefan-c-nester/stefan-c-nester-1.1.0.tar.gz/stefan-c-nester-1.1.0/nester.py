"""Module for iterating through and printing any number of nested lists, Chapter 1 of Head First Python"""

def print_lol(the_list, level):
        for each_item in the_list:
                """The function is recursive, if the current element is a list then the function recurrs - otherwise it prints level number of tabs and then the item"""
                if isinstance(each_item, list):
                        print_lol(each_item, level+1)
                else:
                        for level_num in range(level):
                                print("\t", end='')
                        print(each_item)
