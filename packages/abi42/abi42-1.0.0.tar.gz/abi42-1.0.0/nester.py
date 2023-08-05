"""This module contains a function which prints lists which may/may not include nested lists"""


movies = [
    "The Holy Grail", 1975, "Terry JOnes & Terry Gilliam", 91,
    ["Graham Chapman",
     ["Michael Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]]
]


def print_lol(the_list):
    """This function takes a list argument and each item of the list is printed on the screen in its own line """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
