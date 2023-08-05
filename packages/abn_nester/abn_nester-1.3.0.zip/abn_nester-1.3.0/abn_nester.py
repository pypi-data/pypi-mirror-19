"""this is nester.py  module is used to print lists which have or don't have nested lists"""
def print_lol(the_list,indent= False,level=0):
        """ this function takes the_list (any python list )as argument .when a nested list is encounterd the function recalls itself.level is another argument (used to control tabspaces).Indent is used to control the indentation"""
        for each_item in the_list:
                if isinstance(each_item,list):
                        print_lol(each_item,indent,level+1)
                else:
                        if indent:
                                print("\t"*level,end='')
                          
                                
                        print(each_item)        
        
