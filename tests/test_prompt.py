# TODO: add tests
test_prompts = [
    ("Create a character named Alice from Canada who is a doctor.", True, True, False, True, {'name': 'Alice', 'country': 'Canada', 'profession': 'Doctor'}),
    # ("Generate a character called Bob living in Australia", True, True, False, False, {'name': 'Bob', 'country': 'Australia'}),
    # ("Make a character who is a teacher in Germany.", False, True, False, True, {'country': 'Germany', 'profession': 'Teacher'}),
    # ("Design a new character who is a man", False, False, True, False, {'gender': 'male'}),
    # ("I want to make a new lizard character.", False, False, False, False, {}),
]

    # logger.info(f"actual_aspects: {actual_aspects}")
assert actual_aspects.get("name", False) == prompt[1], f"Name should be detected == {prompt[1]}."
assert actual_aspects.get("country", False) == prompt[2], f"Country should be detected == {prompt[2]}."
assert actual_aspects.get("gender", False) == prompt[3], f"Gender should be detected == {prompt[3]}."
assert actual_aspects.get("profession", False) == prompt[4], f"Profession should be detected == {prompt[4]}."
