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


def is_information_a_sentence(info_text):
    prompt = (
        f"Is the following text a complete sentence or phrase? \"{info_text}\""
        " Respond with True if it is a complete sentence or phrase, otherwise respond with False.")
    sentence_check = dspy.Predict("text: str -> is_sentence: bool", temperature=0.0)
    response = sentence_check(text=prompt, cache=False)
    return response.is_sentence


def extract_most_important_information_from_sentence(info_text, question):
    prompt = (
        f"Given the information: \"{info_text}\", extract the most important information that answers the question: \"{question}\""
        " Provide a concise answer with as few words as possible."
        " Please respond with only the answer, without any additional explanation or context, in as few words as possible.")
    info_extractor = dspy.Predict("text: str -> answer: str", temperature=0.0)
    response = info_extractor(text=prompt, cache=False)
    return response.answer


def check_character_prompt_trait(prompt_text, aspect_question):
        first_prompt = (
            f"Given the prompt: \"{prompt_text}\" can you answer the question: \"{aspect_question}\"?"
            f" Don't include any guesses, supposition or inference beyond what is provided in the prompt about the {aspect_question}."
            " If the prompt does not provide enough information to answer the question, respond with False."
            " If it does, respond with True.")
        # logger.info(f"FIRST: {first_prompt}")
        character_prompt_check = dspy.Predict(CharacterPromptAspect, temperature=0.3)
        check_response = character_prompt_check(request=first_prompt, cache=False)
        detail_exists = check_response.detail_exists
        # logger.info(f"Aspect exists: {detail_exists}")
        return detail_exists


def extract_character_trait(prompt_text, aspect_question):
    prompt = (
        f"Given the prompt: \"{prompt_text}\" answer the question: \"{aspect_question}\""
        f" Don't include any guesses, supposition or inference beyond what is provided in the prompt about the {aspect_question}."
        " If the prompt does not provide enough information to answer the question, respond with 'None'."
        f" If it does, provide a concise answer with as few words as possible giving the {aspect_question} of the character only."
        "Please respond with only the answer, without any additional explanation or context, in as few words as possible.")
    character_prompt = dspy.Predict(CharacterPromptAspect2)
    response = character_prompt(request=prompt, cache=False)
    return_value = ""
    if is_information_a_sentence(response.character_detail):
        # logger.info(f"Full sentence answer detected for aspect {a}, extracting concise information.")
        concise_answer = extract_most_important_information_from_sentence(response.character_detail, aspect_question)
        return_value = concise_answer
        logger.info(f"Concise aspect: {concise_answer}")
    else:
        return_value = response.character_detail
        logger.info(f"Aspect: {response.character_detail}")

    return return_value

def parse_character_prompt(prompt_text):
    answers = {}
    for a, q in QUESTIONS.items():
        detail_exists = check_character_prompt_trait(prompt_text, q)
        if detail_exists:
            aspect_value = extract_character_trait(prompt_text, q)
            answers[a] = aspect_value
        else:
            second_prompt = (
                f"Given the prompt: \"{prompt_text}\" answer the question: \"{q}\""
                f"Why does the prompt not provide enough information to answer the question about the {a} of the character?")
            debug_prompt = dspy.Predict("question: str -> answer: str")
            debug_response = debug_prompt(question=second_prompt, cache=False)
            logger.info(f"DEBUG: {a}: {debug_response.answer}")

            double_check = check_character_prompt_trait(prompt_text, q)
            if double_check:
                aspect_value = extract_character_trait(prompt_text, q)
                answers[a] = aspect_value
    return answers
