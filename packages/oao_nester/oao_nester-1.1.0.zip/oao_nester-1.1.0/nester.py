
# My first python module .for print a  nest list

def print_list(_list,level):
    """

    :param _list:
    :param level:
    :return:
    """
    for item in _list:
        if isinstance(item,list):
            print_list(item,level+1)
        else:
            for tab_stop in range(level):
                print("\t", )
            print(item)


