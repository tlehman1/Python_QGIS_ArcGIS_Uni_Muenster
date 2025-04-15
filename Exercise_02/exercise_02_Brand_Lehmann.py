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
    # Sorting to ensure that all equal numbers are next to each other
    nums.sort()
    # tmp variable to save previous element
    prev = None
    # Result list
    adjNums = []
    # Check if the list has elements
    if len(nums) > 0:
        # Iterate throuh elements of the list
        for num in nums:
            # If the result list is empty, the first item can always be pushed
            if len(adjNums) == 0:
                adjNums.append(num)
            # Checking all other items excluding the first
            else:
                # Since we sorted the list, we can simply check if the current item is bigger than the previous
                # If so, we can add the item to the result since it must be the first of its kind
                # All other items may not be appended
                if num > prev:
                    adjNums.append(num)
            prev = num
    else:
        # Catching emtpy List exception
        return "Input list is empty"
    return adjNums


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