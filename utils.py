import re


# Returns list of all floats in string
def extract_floats(s):
    return [float(num) for num in re.findall("\d+\.\d+", s)]


# Returns list of all floats or integers in string
def extract_nums(s):
    strings = re.findall("\d*\.\d+|\d+", s)
    nums = []
    for string in strings:
        try:
            nums.append(int(string.encode("utf-8")))
        except ValueError:
            nums.append(float(string.encode("utf-8")))
    return nums


# Returns list of sequences in a string that match the pattern of an integer followed by a word
def find_time_periods(s):
    strings = re.findall(" \d+.[a-z]+", s.replace(u'\xa0', u' '))
    periods = []
    for string in strings:
        periods.append((re.findall("[a-z]+", string)[0], int(re.findall("\d+", string)[0])))
    return periods
