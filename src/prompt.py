import dspy

from utils import get_logger

logger = get_logger(__file__)

QUESTIONS = {
    "name": "Do you know the name of the character?",
    "country": "Do you know the country the character is from?",
    "gender": "Do you know the character's gender?",
    "profession": "Do you know the character's profession?",
}


class CharacterPromptAspect(dspy.Signature):
    request: str = dspy.InputField()
    detail_exists: bool = dspy.OutputField()


class CharacterPromptAspect2(dspy.Signature):
    request: str = dspy.InputField()
    character_detail: str = dspy.OutputField()


def parse_character_prompt(prompt_text):
    answers = {}
    for a, q in QUESTIONS.items():
        first_prompt = (
            f"Given the prompt: \"{prompt_text}\" can you answer the question: \"{q}\"?"
            f" Don't include any guesses, supposition or inference beyond what is provided in the prompt about the {a}."
            " If the prompt does not provide enough information to answer the question, respond with False."
            " If it does, respond with True.")
        # logger.info(f"FIRST: {first_prompt}")
        character_prompt_check = dspy.Predict(CharacterPromptAspect)
        check_response = character_prompt_check(request=first_prompt, cache=False)
        detail_exists = check_response.detail_exists
        logger.info(f"Aspect exists: {detail_exists}")

        if detail_exists:
            second_prompt = (
            f"Given the prompt: \"{prompt_text}\" answer the question: \"{q}\""
            f" Don't include any guesses, supposition or inference beyond what is provided in the prompt about the {a}."
            " If the prompt does not provide enough information to answer the question, respond with 'None'."
            f" If it does, provide a concise answer with as few words as possible giving the {a} of the character.")
            # logger.info(f"SECOND: {second_prompt}")
            character_prompt = dspy.Predict(CharacterPromptAspect2)
            response = character_prompt(request=second_prompt, cache=False)
            print(response.history)
            answers[a] = response.character_detail
            logger.info(f"Aspect: {response.character_detail}")
        else:
            second_prompt = (
                f"Given the prompt: \"{prompt_text}\" answer the question: \"{q}\""
                f"Why does the prompt not provide enough information to answer the question about the {a} of the character?")
            debug_prompt = dspy.Predict("question: str -> answer: str")
            debug_response = debug_prompt(question=second_prompt, cache=False)
            logger.info(f"DEBUG: {debug_response.answer}")

            debug_prompt2 = dspy.Predict("question: str -> answer: list[str]")
            debug_response2 = debug_prompt2(
                question=f"What information and facts are listed in the text: \"{prompt_text}\" that relate to the {a} of the character?", 
                cache=False)
            logger.info(f"DEBUG: {debug_response2.answer}")
    return answers
