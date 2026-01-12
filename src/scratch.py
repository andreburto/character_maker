import os

from utils import (get_logger, get_database_connection, initialize_database, 
                   fetch_oldest_unprocessed_prompt)

logger = get_logger(__file__)


def main():
    db_path = os.path.join(os.path.dirname(__file__), 'test_character_maker.db')
    if not os.path.exists(db_path):
        initialize_database(db_path)

    connection = get_database_connection(db_path)
    prompt = fetch_oldest_unprocessed_prompt(connection)
    if prompt:
        logger.info(f"Oldest unprocessed prompt: {prompt}")
    else:
        logger.info("No unprocessed prompts found.")
    connection.close()


if __name__ == "__main__":
    main()
