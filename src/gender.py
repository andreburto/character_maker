import dspy


class GenderMale(dspy.Signature):
    name: str = dspy.InputField()
    is_male: bool = dspy.OutputField()


class GenderFemale(dspy.Signature):
    name: str = dspy.InputField()
    is_female: bool = dspy.OutputField()


def get_gender_of_name(name):
    male_prompt = f"Is the name {name} typically a male name?"
    female_prompt = f"Is the name {name} typically a female name?"

    gender_male = dspy.Predict(GenderMale)
    male_response = gender_male(name=male_prompt, cache=False)

    if male_response.is_male:
        return 'male'
    else:
        gender_female = dspy.Predict(GenderFemale)
        female_response = gender_female(name=female_prompt, cache=False)
        if female_response.is_female:
            return 'female'
        else:
            return 'other'