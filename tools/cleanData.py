import re

def filter_list_by_regex(string_list, regex):
    #Function that can remove all lists in a string that do not follow the given regular expression.
    filtered_list = []
    pattern = re.compile(regex)
    for string in string_list:
        if pattern.match(string):
            filtered_list.append(string)
    return filtered_list
