"""This is the nester module, and it provide you a function called print_lol()
which can print the lists that may or may not have nested list.
"""
def print_lol(the_list):
    """ :param custom_list:the list you wanna print
        :return:each item per line
    """
    
    for each_items in the_list:
        if isinstance(each_items, list):
            print_lol(each_items)
        else:
            print(each_items)
