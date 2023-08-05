
# My first python module .for print a  nest list

def print_list(_list):
    """
    :param _list:
    :return: print nest list
    """
    for item in _list:
        if isinstance(item,list):
            print_list(item)
        else:
            print(item)


