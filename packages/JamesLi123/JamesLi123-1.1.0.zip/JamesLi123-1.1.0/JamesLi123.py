"""This is "nester.py" module, which provides a function named print_lol(). This function is uesd
to print the list, including(or not) nested list."""


def print_lol(the_list):
    """This function has a location parameter named "the_list", and it is any Python list(maybe a
    list including nested list). Each data item of the specified list will be printed to the screen
    (recursively), and each item will occupy a line space respectively."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)