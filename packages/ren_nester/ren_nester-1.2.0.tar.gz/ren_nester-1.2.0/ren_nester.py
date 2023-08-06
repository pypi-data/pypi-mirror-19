"""This is the nester module, and it provide you a function called print_lol()
which can print the lists that may or may not have nested list.
Provided in the list of the various data items will be printed to the screen, and a line
"""
def print_lol(the_list,level=0):
    """ :param custom_list:the list you wanna print
        :return:each item per line
    """
    
    for each_items in the_list:
        if isinstance(each_items, list):
            print_lol(each_items,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(each_items)
