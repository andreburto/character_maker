import datetime
import dspy
import os
import random
import sys

from country import is_country_american, get_country_choice, update_countries_file
from gender import get_gender_of_name
from name import get_name_from_american, get_name_from_international
from prompt import parse_character_prompt, check_character_prompt_for_detail, QUESTIONS
from utils import (initialize_database, get_database_connection, close_database_connection, 
                   insert_prompt_into_db, fetch_oldest_unprocessed_prompt, insert_character_trait_into_db,
                   mark_prompt_as_processed, get_character_traits_by_prompt_id, get_logger)

logger = get_logger(__file__)


def make_the_character(properties):
    """
    Docstring for make_the_character
    
    :param properties: Description
    """
    character_details = {}
    character_details.update(properties)
    logger.info(f"Making character with initial properties: {properties}")
    logger.info(f"Starting character details: {character_details}")

    if 'country' in properties.keys():
        character_details['country'] = properties['country']
    else:
        character_details['country'] = get_country_choice()

    if 'name' in properties.keys():
        character_details['name'] = properties['name']
    else:
        if is_country_american(character_details['country']):
            f, m, l = get_name_from_american()
            character_details['name'] = f"{f} {m} {l}"
        else:
            character_details['name'] = get_name_from_international(character_details['country'])
            update_countries_file(character_details['country'])

    if 'gender' in properties:
        character_details['gender'] = properties['gender']
    else:
        character_details['gender'] = get_gender_of_name(
            character_details['name'], character_details['country'])

    if 'profession' in properties.keys():
        character_details['profession'] = properties['profession']
    else:
        character_details['profession'] = "TODO: Generate profession"

    return character_details


def main():
    start_time = datetime.datetime.now()
    random.seed(int(datetime.datetime.now().microsecond))

    # Configure dspy
    dspy.configure(lm=dspy.LM('ollama_chat/llama3.2', api_base='http://localhost:11434'))
    dspy.configure_cache(enable_disk_cache=False, enable_memory_cache=False,)

    db_path = os.path.join(os.path.dirname(__file__), 'test_character_maker.db')
    if os.path.exists(db_path):
        os.remove(db_path)

    initialize_database(db_path)
    db_conn = get_database_connection(db_path)

    test_prompts = [
        ("Create a character named Alice from Canada who is a doctor.", True, True, False, True, {'name': 'Alice', 'country': 'Canada', 'profession': 'Doctor'}),
        # ("Generate a character called Bob living in Australia", True, True, False, False, {'name': 'Bob', 'country': 'Australia'}),
        # ("Make a character who is a teacher in Germany.", False, True, False, True, {'country': 'Germany', 'profession': 'Teacher'}),
        # ("Design a new character who is a man", False, False, True, False, {'gender': 'male'}),
        # ("I want to make a new lizard character.", False, False, False, False, {}),
    ]

    for prompt in test_prompts:
        actual_aspects = {}
        logger.info("-----")
        logger.info(f"Prompt: {prompt[0]}")
        prompt_id = insert_prompt_into_db(db_conn, prompt[0])

        prompt_data = fetch_oldest_unprocessed_prompt(db_conn)
        assert prompt_data is not None, "Failed to fetch the inserted prompt."  
        logger.info(f"Fetched prompt from DB: {prompt_data}")

        for t in QUESTIONS.keys():
            if check_character_prompt_for_detail(prompt[0], t):
                # logger.info(f"Aspect {t} exists.")
                actual_aspects[t] = True
        # logger.info(f"actual_aspects: {actual_aspects}")
        assert actual_aspects.get("name", False) == prompt[1], f"Name should be detected == {prompt[1]}."
        assert actual_aspects.get("country", False) == prompt[2], f"Country should be detected == {prompt[2]}."
        assert actual_aspects.get("gender", False) == prompt[3], f"Gender should be detected == {prompt[3]}."
        assert actual_aspects.get("profession", False) == prompt[4], f"Profession should be detected == {prompt[4]}."
        character_info = parse_character_prompt(prompt[0])
        print(f"Extracted character info: {character_info}")
        for k, v in prompt[5].items():
            assert character_info.get(k, None).lower() == v.lower(), f"Expected {k} to be {v}, got {character_info.get(k, None)}"
            if character_info.get(k):
                insert_character_trait_into_db(db_conn, prompt_id, k, character_info.get(k))
        trait_data = get_character_traits_by_prompt_id(db_conn, prompt_id)
        logger.info(f"Stored traits in DB: {trait_data}")
        new_character = make_the_character(character_info)
        logger.info(f"Final character generated: {new_character}")
        mark_prompt_as_processed(db_conn, prompt_id)  

    logger.info("-----")
    finish_time = datetime.datetime.now()
    elapsed = finish_time - start_time
    logger.info(f"All tests passed in {elapsed.total_seconds()} seconds.")
    close_database_connection(db_conn)


if __name__ == '__main__':
    main()
