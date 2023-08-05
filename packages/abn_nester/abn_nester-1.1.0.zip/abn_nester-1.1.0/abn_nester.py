"""this is nester.py  module is used to print lists which have or don't have nested lists"""
def print_lol(the_list,level):
        """ this function takes the_list (any python list )as argument .when a nested list is encounterd the function recalls itself"""
        for each_item in the_list:
                if isinstance(each_item,list):
                        print_lol(each_item,level+1)
                else:
                        for tabs in range(level):
                                print("\t",end='')
                        print(each_item)        
        
