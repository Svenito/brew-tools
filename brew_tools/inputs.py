from typing import Callable, List


def get_choice(prompt: str, choices: List[str]) -> int:
    num_choices = len(choices)
    valid_range = between(-1, num_choices)
    while True:
        for i, choice in enumerate(choices):
            print(f"{i}: {choice}")

        answer = int(input(f"{prompt}\n"))
        if valid_range(answer):
            return answer
        print("Invalid selection.")


def between(min: float, max: float) -> Callable:
    """
    Returns a function to test if a value lies between min and max
    """

    def op(x):
        if min < x and x < max:
            return True
        print("ERROR: Value must be between {} and {}".format(min, max))
        return False

    return op


def get_unit_input(unit: str, prompt: str) -> float:
    """
    Prompt for an input for temperature and automatically resolve
    unit (Celcius or Fahrenheit)

    :arg unit: unit to use
    :arg prompt: User prompt. Correct unit will be appended
    :return: entered value as float
    """
    prompt = "{prompt} ({units}): ".format(prompt=prompt, units=unit)
    value = float(input(prompt))

    return value


def get_gravity_input(prompt: str) -> float:
    """
    Prompt for an input for gravity and validated to be
    between 1.0 and 1.2

    :arg ctx: Click context
    :arg prompt: User prompt. Will be checked for bounds
    :return: entered value as float
    """
    valid_range = between(1.0, 1.2)
    gravity = float(input(prompt))
    valid_range(gravity)

    return gravity
