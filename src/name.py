import dspy


class AmericanName(dspy.Signature):
    request: str = dspy.InputField()
    first: str = dspy.OutputField()
    middle: str = dspy.OutputField()
    last: str = dspy.OutputField()


class InternationalName(dspy.Signature):
    request: str = dspy.InputField()
    full_name: str = dspy.OutputField()


def get_name_from_international(country_name):
    name_prompt = (
        f"Provide a typical full name from {country_name} at random."
        " Only provide the full name as a string. No formatting. On a single line")
    international_name = dspy.Predict(InternationalName)
    response = international_name(request=name_prompt, cache=False)
    return response.full_name


def get_name_from_american():
    name_prompt = "Provide a typical American full name with first, middle, and last names at random."
    american_name = dspy.Predict(AmericanName)
    response = american_name(request=name_prompt, cache=False)
    return response.first, response.middle, response.last