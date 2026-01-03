import datetime
import dspy
import random
# import sys

from country import is_country_american, get_country_choice, update_countries_file
from gender import get_gender_of_name
from name import get_name_from_american, get_name_from_international
from prompt import parse_character_prompt, check_character_prompt_for_detail, QUESTIONS
from utils import get_logger


logger = get_logger(__file__)


def test_main():
    start_time = datetime.datetime.now()
    dspy.configure(lm=dspy.LM('ollama_chat/llama3.2', api_base='http://localhost:11434'))
    dspy.configure_cache(enable_disk_cache=False, enable_memory_cache=False,)

    test_prompts = [
        ("Create a character named Alice from Canada who is a doctor.", True, True, False, True, {'name': 'Alice', 'country': 'Canada', 'profession': 'Doctor'}),
        ("Generate a character called Bob living in Australia", True, True, False, False, {'name': 'Bob', 'country': 'Australia'}),
        ("Make a character who is a teacher in Germany.", False, True, False, True, {'country': 'Germany', 'profession': 'Teacher'}),
        ("Design a new character who is a man", False, False, True, False, {'gender': 'male'}),
        ("I want to make a new lizard character.", False, False, False, False, {}),
    ]

    for prompt in test_prompts:
        aspect_count = 0
        actual_aspects = {}
        logger.info("-----")
        logger.info(f"Prompt: {prompt[0]}")
        for t in QUESTIONS.keys():
            if check_character_prompt_for_detail(prompt[0], t):
                logger.info(f"Aspect {t} exists.")
                actual_aspects[t] = True
        logger.info(f"actual_aspects: {actual_aspects}")
        assert actual_aspects.get("name", False) == prompt[1], f"Name should be detected == {prompt[1]}."
        assert actual_aspects.get("country", False) == prompt[2], f"Country should be detected == {prompt[2]}."
        assert actual_aspects.get("gender", False) == prompt[3], f"Gender should be detected == {prompt[3]}."
        assert actual_aspects.get("profession", False) == prompt[4], f"Profession should be detected == {prompt[4]}."
        logger.info("-")
        character_info = parse_character_prompt(prompt[0])
        for k, v in prompt[5].items():
            assert character_info.get(k, None).lower() == v.lower(), f"Expected {k} to be {v}, got {character_info.get(k, None)}"
        print(f"Extracted character info: {character_info}")
        # assert len(character_info.keys()) == prompt[1], f"Expected {prompt[1]} aspects, got {len(character_info)}"
    logger.info("-----")
    finish_time = datetime.datetime.now()
    elapsed = finish_time - start_time
    logger.info(f"All tests passed in {elapsed.total_seconds()} seconds.")


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
