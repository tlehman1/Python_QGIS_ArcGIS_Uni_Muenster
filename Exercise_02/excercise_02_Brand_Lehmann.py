# donuts
# Given an integer count of a number of donuts, return a string
# of the form 'Number of donuts: <count>', where <count> is the number
# passed in. However, if the count is 10 or more, then use the word'many'
# instead of the actual count.
# So donuts(5) returns 'Number of donuts: 5'
# and donuts(23) returns 'Number of donuts: many'
def donuts(count):
    # check if the input is an Integer with isinstance()
    if isinstance(count, int):
        # if the number of donuts is 10 or larger it returns 'many'
        if count >= 10:
            return 'Number of donuts: many'
        # if the number of donuts is under 10 it returns the actual number of donuts given
        else:
            return f'Number of donuts: {count}'
    # when the input =! Integer, an error message is displayed
    else:
        return 'Give a valid Number'


# verbing
# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
def verbing(s):
    # Check if s is a string to avoid errors while concatinating strings and numbers
    if isinstance(s, str):
        # Check if s is longer than 2 characters
        if len(s) > 2:
            s = s.lower() # to lower to avoid mismatches due to case sensitivity
            # When s ends with 'ing', 'ly' is added. This needs to be checked first 
            if s.endswith('ing'):
                s = s + 'ly'
            # If s does not ends with 'ing', it needs to be added
            else:
                s = s + 'ing'
    return s


# Remove adjacent
# Given a list of numbers, return a list where
# all adjacent == elements have been reduced to a single element,
# so [1, 2, 2, 3] returns [1, 2, 3]. You may create a new list or
# modify the passed in list.
def remove_adjacent(nums):
# +++your code here+++
    return


def main():
    print('donuts')
    print(donuts(4))
    print(donuts(9))
    print(donuts(10))
    print(donuts('twentyone'))
    print('verbing')
    print(verbing('hail'))
    print(verbing('swiming'))
    print(verbing('do'))
    print('remove_adjacent')
    print(remove_adjacent([1, 2, 2, 3]))
    print(remove_adjacent([2, 2, 3, 3, 3]))
    print(remove_adjacent([]))
# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()