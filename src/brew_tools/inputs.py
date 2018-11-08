def is_metric(ctx):
    return ctx.obj['unit'] == 'metric'


def is_imperial(ctx):
    return not is_metric(ctx)


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
    while 1:
        try:
            value = input(prompt)
            value = operation(value)
            if check:
                if not check(value):
                    raise Exception
            return value
        except (ValueError, Exception):
            continue


def get_unit_input(unit, prompt):
    """
    Prompt for an input for temperature and automatically resolve
    unit (Celcius or Fahrenheit)

    :arg ctx: Click context
    :arg prompt: User prompt. Correct unit will be appended
    :return: entered value as float
    """
    prompt = "{prompt} ({units}): ".format(prompt=prompt, units=unit)
    value = get_input(prompt, lambda x: float(x))

    return value


def get_gravity_input(ctx, prompt):
    """
    Prompt for an input for gravity and validated to be
    between 1.0 and 1.2

    :arg ctx: Click context
    :arg prompt: User prompt. Will be checked for bounds
    :return: entered value as float
    """
    valid_range = between(1.0, 1.2)
    gravity = get_input(prompt, lambda x: float(x), valid_range)

    return gravity
