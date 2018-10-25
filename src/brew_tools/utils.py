def between(min, max):
    def op(x):
        if min < x and x < max:
            return True
        print("ERROR: Value must be between {} and {}".format(min, max))
        return False
    return op


def get_input(prompt, operation, check=None):
    """
    Prompt the user for a gravity input. Converts input to float and checks
    bounds of 1.000 and 1.200.
    If value is invalid it will re-prompt user
    """
    try:
        value = input(prompt)
        value = operation(value)
        if check:
            if not check(value):
                raise Exception
    except (ValueError, Exception):
        value = get_input(prompt, operation, check)

    return value
