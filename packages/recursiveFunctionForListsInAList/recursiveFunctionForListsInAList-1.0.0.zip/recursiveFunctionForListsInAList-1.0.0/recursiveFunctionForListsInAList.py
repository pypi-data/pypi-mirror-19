# Example from Head First
# Reference - Chapter 2

"""This is the "recursiveFunctionForListsInAList.py" module, and it provides a function
called print_list() which prints lists that may or may not include nested lists."""

def print_list(the_list):
    """This function takes a positional argument called 'inner list', which is any Python list (of, possibly, nested lists).
    Each data item in the provided list is (recursively) printed to the screen on its own line."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_list(each_item)
        else:
            print(each_item)
