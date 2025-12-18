import datetime
import dspy
import random

from country import is_country_american, get_country_choice, update_countries_file
from gender import get_gender_of_name
from name import get_name_from_american, get_name_from_international


def main():
    random.seed(int(datetime.datetime.now().microsecond))

    dspy.configure(lm=dspy.LM('ollama_chat/llama3.2', api_base='http://localhost:11434'))
    dspy.configure_cache(enable_disk_cache=False, enable_memory_cache=False,)

    country = get_country_choice()

    if is_country_american(country):
        f, m, l = get_name_from_american()
        character_name = f"{f} {m} {l}"
    else:
        character_name = get_name_from_international(country)
        update_countries_file(country)

    gender = get_gender_of_name(character_name.split()[0])

    print(f"Generated character from {country}: {character_name} (Gender: {gender})")


if __name__ == '__main__':
    main()
