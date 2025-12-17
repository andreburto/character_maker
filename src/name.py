import dspy


class AmericanName(dspy.Signature):
    request: str = dspy.InputField()
    first: str = dspy.OutputField()
    middle: str = dspy.OutputField()
    last: str = dspy.OutputField()


class InternationalName(dspy.Signature):
    request: str = dspy.InputField()
    full_name: str = dspy.OutputField()
