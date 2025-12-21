import datetime
import dspy
import logging
import random
import sys

from country import is_country_american, get_country_choice, update_countries_file
from gender import get_gender_of_name
from name import get_name_from_american, get_name_from_international
from prompt import parse_character_prompt
from utils import get_logger


logger = get_logger(__file__)


def test_main():
    dspy.configure(lm=dspy.LM('ollama_chat/llama3.2', api_base='http://localhost:11434'))
    dspy.configure_cache(enable_disk_cache=False, enable_memory_cache=False,)

    test_prompts = [
        ("Create a character named Alice from Canada who is a doctor.", 3),
        ("Generate a character called Bob living in Australia", 2),
        ("Make a character who is a teacher in Germany.", 2),
        ("Design a new character", 0),
    ]

    for prompt in test_prompts:
        character_info = parse_character_prompt(prompt[0])
        logger.info(f"Prompt: {prompt[0]}")
        logger.info(f"Character Info: {character_info}")
        assert len(character_info.keys()) == prompt[1], f"Expected {prompt[1]} aspects, got {len(character_info)}"
        print("-----")


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

    gender = get_gender_of_name(character_name, country)

    print(f"Generated character from {country}: {character_name} (Gender: {gender})")


if __name__ == '__main__':
    test_main()
    # main()
