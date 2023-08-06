"""This is "nester.py" module, which provides a function named print_lol(). This function is uesd
to print the list, including(or not) nested list."""


def print_lol(the_list, level):
    """This function has a location parameter named "the_list", and it is any Python list(maybe a
    list including nested list). Each data item of the specified list will be printed to the screen
    (recursively), and each item will occupy a line space respectively. The second argument(named
    "level") is used to insert TAB when it meets nested lists."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)