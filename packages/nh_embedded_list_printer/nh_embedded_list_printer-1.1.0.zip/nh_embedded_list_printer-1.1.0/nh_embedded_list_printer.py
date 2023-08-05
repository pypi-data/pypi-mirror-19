"""
@author:   Nick Handy
@date:     12/28/16
@summary:  This module takes in a list and prints out each element. This method can handle
           nested lists. 
"""
from __future__ import print_function

def print_lol(the_list, level):
    for each_item in the_list:
        """This function takes in a list object "the_list" which may or may not be a 
           nested list. Each item within the list is printed through the recursive 
           steps below"""
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end =" ")
            print(each_item)
