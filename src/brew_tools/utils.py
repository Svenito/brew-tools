def between(min, max):
    """
    Returns a function to test if a value lies between min and max
    """
    def op(x):
        if min < x and x < max:
            return True
        print("ERROR: Value must be between {} and {}".format(min, max))
        return False
    return op


def get_input(prompt, operation, check=None):
    """
    Prompt the user for input and apply ``operation`` to input.
    If ``check`` is not None run the check on the converted input

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


def get_vol_input(ctx, prompt):
    unit = ctx.obj["units"]["vol"]
    prompt = "{prompt} ({units}) :".format(prompt=prompt, units=unit)
    vol = get_input(prompt, lambda x: float(x))

    return vol


def get_gravity_input(ctx, prompt):
    valid_range = between(1.0, 1.2)
    og = get_input(prompt, lambda x: float(x), valid_range)

    return og
