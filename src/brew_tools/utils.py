def between(min, max):
    def op(x):
        return min < x and x < max
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
        print("ERROR: Value must be between 1.000 and 1.200")
        value = get_input(prompt, operation, check)

    return value
