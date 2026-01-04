import logging
import sqlite3
import sys

from datetime import datetime
from uuid import uuid4

logger = logging.getLogger(__name__)

DATABASE_SCHEMA = """
CREATE TABLE IF NOT EXISTS prompts (
    id TEXT PRIMARY KEY,
    prompt_text TEXT NOT NULL,
    is_processed BOOLEAN NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS character_traits (
    id TEXT PRIMARY KEY,
    prompt_id TEXT NOT NULL,
    trait_type TEXT NOT NULL,
    trait_value TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (prompt_id) REFERENCES prompts (id)
);
"""


def get_logger(identifier):
    logger = logging.getLogger(identifier)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    return logger


def get_database_connection(db_path):
    connection = sqlite3.connect(db_path)
    return connection


def close_database_connection(connection):
    if connection:
        connection.close()


def initialize_database(db_path):
    connection = get_database_connection(db_path)
    cursor = connection.cursor()
    cursor.executescript(DATABASE_SCHEMA)
    connection.commit()
    close_database_connection(connection)


def insert_prompt_into_db(connection, prompt_text):
    cursor = connection.cursor()
    prompt_id = str(uuid4())
    cursor.execute(
        """
        INSERT INTO prompts (id, prompt_text, is_processed, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (prompt_id, prompt_text, False, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ))
    connection.commit()
    return prompt_id


def get_prompt_by_id(connection, prompt_id):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, prompt_text, is_processed, created_at
        FROM prompts
        WHERE id = ?
        """,
        (prompt_id, ))
    row = cursor.fetchone()
    if row:
        return {
            "id": row[0],
            "prompt_text": row[1],
            "is_processed": row[2],
            "created_at": row[3], }
    return None


def mark_prompt_as_processed(connection, prompt_id):
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE prompts
        SET is_processed = ?
        WHERE id = ?
        """,
        (True, prompt_id))
    connection.commit()


def fetch_oldest_unprocessed_prompt(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, prompt_text
        FROM prompts
        WHERE is_processed = ?
        ORDER BY created_at ASC
        LIMIT 1
        """,
        (False, ))
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "prompt_text": row[1]}
    return None


def insert_character_trait_into_db(connection, prompt_id, trait_type, trait_value):
    cursor = connection.cursor()
    trait_id = str(uuid4())
    cursor.execute(
        """
        INSERT INTO character_traits (id, prompt_id, trait_type, trait_value, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            trait_id,
            prompt_id,
            trait_type,
            trait_value,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ))
    connection.commit()
    return trait_id


def get_character_traits_by_prompt_id(connection, prompt_id):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT trait_type, trait_value
        FROM character_traits
        WHERE prompt_id = ?
        """,
        (prompt_id, ))
    rows = cursor.fetchall()
    traits = {}
    for row in rows:
        traits[row[0]] = row[1]
    return traits