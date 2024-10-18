from typing import TypeVar, Callable, List


T = TypeVar("T")


def get_valid_input(prompt: str, valid_range: Callable[[float], bool] | None = None):
    while True:
        user_input = input(prompt)
        try:
            output_value = float(user_input)
        except ValueError:
            print(f"ERROR: {user_input} is not valid.")
            continue

        if valid_range:
            if not valid_range(output_value):
                continue
        return output_value


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


def between(min_value: float, max_value: float) -> Callable:
    """
    Returns a function to test if a value lies between min and max
    """

    def op(x):
        if min_value < x < max_value:
            return True
        print("ERROR: Value must be between {} and {}".format(min_value, max_value))
        return False

    return op


def get_input(prompt: str, convert: Callable[[str], T]) -> T:
    """
    Runs a convert function on a prompt
    """
    return convert(input(prompt))


def get_unit_input(unit: str, prompt: str) -> float:
    """
    Prompt for an input for temperature and automatically resolve
    unit (Celcius or Fahrenheit)

    :arg unit: unit to use
    :arg prompt: User prompt. Correct unit will be appended
    :return: entered value as float
    """
    prompt = "{prompt} ({units}): ".format(prompt=prompt, units=unit)
    return get_valid_input(prompt)


def get_gravity_input(prompt: str) -> float:
    """
    Prompt for an input for gravity and validated to be
    between 1.0 and 1.2

    :arg prompt: User prompt. Will be checked for bounds
    :return: entered value as float
    """
    valid_range = between(1.0, 1.2)
    return get_valid_input(prompt, valid_range)
