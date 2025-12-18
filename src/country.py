import datetime
import dspy
import random


class ChooseCountry(dspy.Signature):
    request: str = dspy.InputField()
    country: str = dspy.OutputField()


class IdentifyAmerica(dspy.Signature):
    request: str = dspy.InputField()
    is_american: bool = dspy.OutputField()


def get_country_choice():
    existing_countries = get_country_list()
    extra_rule = f" Exclude these countries in the following list: {', '.join(existing_countries)}." \
        if existing_countries else ""

    chose_prompt = (
        f"{datetime.datetime.now()}: Name single a country at random somewhere in the world."
        f" Display only the country name. No additional text or formatting. {extra_rule}")
    choose_country = dspy.Predict(ChooseCountry, temperature=random.uniform(0.1, 0.9))
    choose_country_response = choose_country(request=chose_prompt, cache=False)
    return choose_country_response.country


def is_country_american(country_name):
    prompt = f"Is {country_name} the same country as the United States of America?"
    identify_america = dspy.Predict(IdentifyAmerica)
    response = identify_america(request=prompt, cache=False)
    return response.is_american


def get_country_list():
    try:
        with open('countries.txt', 'r') as file:
            countries = [line.strip() for line in file.readlines()]
        return countries
    except FileNotFoundError:
        return []
    

def update_countries_file(country):
    countries = list(set([country] + get_country_list()))
    countries_to_save = countries if len(countries) <= 5 else countries[:-1]
    with open('countries.txt', 'w') as file:
        for c in countries_to_save:
            file.write(f"{c}\n")
