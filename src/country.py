import dspy


class ChooseCountry(dspy.Signature):
    request: str = dspy.InputField()
    country: str = dspy.OutputField()


class IdentifyAmerica(dspy.Signature):
    request: str = dspy.InputField()
    is_american: bool = dspy.OutputField()


def get_country_list():
    try:
        with open('countries.txt', 'r') as file:
            countries = [line.strip() for line in file.readlines()]
        return countries
    except FileNotFoundError:
        return []
    

def update_countries_file(country):
    countries = list(set([country] + get_country_list()))
    print(f"Updated country list: {countries}")
    countries_to_save = countries if len(countries) <= 5 else countries[:-1]
    print(f"Saving countries: {countries_to_save}")
    with open('countries.txt', 'w') as file:
        for c in countries_to_save:
            file.write(f"{c}\n")
