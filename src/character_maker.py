import datetime
import dspy
import random

from country import ChooseCountry, IdentifyAmerica, get_country_list, update_countries_file
from name import AmericanName, InternationalName
from utils import llm_debug


def main():
    random.seed(int(datetime.datetime.now().microsecond))

    dspy.configure(lm=dspy.LM('ollama_chat/llama3.2', api_base='http://localhost:11434'))
    dspy.configure_cache(enable_disk_cache=False, enable_memory_cache=False,)

    existing_countries = get_country_list()
    extra_rule = f" Exclude these countries in the following list: {', '.join(existing_countries)}." if existing_countries else ""

    chose_prompt = (
        f"{datetime.datetime.now()}: Name single a country at random somewhere in the world."
        f" Display only the country name. No additional text or formatting. {extra_rule}")
    choose_country = dspy.Predict(ChooseCountry, temperature=random.uniform(0.1, 0.9))
    choose_country_response = choose_country(request=chose_prompt, cache=False)
    llm_debug(chose_prompt, choose_country_response.country)

    id_usa_prompt = f"Is {choose_country_response.country} the same country as the United States of America?"
    identify_america = dspy.Predict(IdentifyAmerica)
    identify_america_response = identify_america(request=id_usa_prompt, cache=False)
    llm_debug(id_usa_prompt, identify_america_response.is_american)

    if not identify_america_response.is_american:
        update_countries_file(choose_country_response.country)

    if identify_america_response.is_american:
        name_prompt = "Provide a typical American full name with first, middle, and last names at random."
        american_name = dspy.Predict(AmericanName)
        american_name_response = american_name(request=name_prompt, cache=False)
        llm_debug(name_prompt, f"{american_name_response.first} {american_name_response.middle} {american_name_response.last}")
    else:
        name_prompt = (
            f"Provide a typical full name from {choose_country_response.country} at random."
            " Only provide the full name as a string. No formatting.")
        international_name = dspy.Predict(InternationalName)
        international_name_response = international_name(request=name_prompt, cache=False)
        llm_debug(name_prompt, international_name_response.full_name)


if __name__ == '__main__':
    main()
