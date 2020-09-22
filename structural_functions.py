def get_closest_value(arr, target):
    """From a list of values choose one closest to a target number."""
    n = len(arr)
    left = 0
    right = n - 1
    mid = 0

    # search edge case - last or above all or
    if target >= arr[n - 1]:
        return arr[n - 1]
    # search edge case - first or below all.
    if target <= arr[0]:
        return arr[0]
    # BSearch solution: Time & Space: Log(N)
    while left < right:
        mid = (left + right) // 2  # find the mid
        if target < arr[mid]:
            right = mid
        elif target > arr[mid]:
            left = mid + 1
        else:
            return arr[mid]

    if target < arr[mid]:
        return find_closest(arr[mid - 1], arr[mid], target)
    else:
        return find_closest(arr[mid], arr[mid + 1], target)


def find_closest(val1, val2, target):
    """Contain get_closest value to a certain target."""
    return val2 if target - val1 >= val2 - target else val1


def getKeyByValue(dictOfElements, valueToFind):
    """Get the first key that contains the specified value."""
    for key, value in dictOfElements.items():
        if value == valueToFind:
            return key


def mergeDicts(dict1, dict2):
    """Merge two dictionaries."""
    res = {**dict1, **dict2}
    return res


def testInput(verificationFunction):
    """Unitesting for inputs."""
    while True:
        result = input()
        if verificationFunction(result):
            return result
        else:
            print("Invalid input, try again")
