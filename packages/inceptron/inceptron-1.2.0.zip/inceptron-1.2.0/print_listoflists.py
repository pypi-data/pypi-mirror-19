
"""
This is the “inceptron.py" module, and it provides the following functions
print_listoflists() which prints lists that may or may not include nested lists.
sanitize() which returns cleansed list without no colons or dashes.
"""

def print_list(llist, indent=False, level=0):
    """
    This function takes a positional argument called “llist", which is any
    Python list (of, possibly, nested lists). Each data item in the provided list
    is (recursively) printed to the screen on its own line.
    :param llist:
    :param indent:
    :param level:
    :return:
    """
    for each_item in llist:
        if isinstance(each_item, list):
            print_list(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='')
            print(each_item)

def sanitize(time_String):
    """
    This function takes input as string from each list(s). And then processes
    the string to replace any dashes or colons with '.' period and returns the
    sanitized list(s).
    :param time_String:
    :return:
    """
    if '-' in time_String:
        splitter = '-'
    elif ':' in time_String:
        splitter = ':'
    else:
        return(time_String)
    (mins, secs) = time_String.split(splitter)
    return(mins + '.' + secs)

class AthleteList(list):
    """
    This class has inherited the built-in list class in-order to avoid coding extraneous codes.
     top3 - this is a function to provide the first three components of a list in a sorted manner.
    """
    def __init__(self, a_name, a_dob=None, a_times=[]):
        list.__init__([])
        self.name = a_name
        self.dob  = a_dob
        self.extend(a_times)
    def top3(self):
        return(sorted(set([sanitize(t) for t in self]))[0:3])