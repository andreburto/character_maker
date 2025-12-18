# Character Maker

## About

Using [DSPy](https://dspy.ai/), [Ollma](https://ollama.com/), and the [Llama 3.2 model](https://ollama.com/library/llama3.2) to create a simple character creator.
It's the biggest model my potato computer will run, but the purpose of this is to see how far I can push smaller models. It's fine. &lt;/cope&gt;

# Usage

1. Install Python 3.11 or later.
2. Run `python3 -m pip install requirements.txt` to install required libraries.
3. Download and install Ollama.
4. Use Ollama to install the `ollama_chat/llama3.2` model.
5. `cd src` and `python3 character_maker.py` to generate a character.

## To Do

1. Reinstate `llm_debug` to show prompts when debugging.
2. Add more character attributes to the workflow.
3. Use sqlite to store characters.
4. Add a web form to make creating characters easier.
5. Replace the `get_country_choice` with a random picker from a list, but have an LLM generate the list.
6. Turn this into a serverless app.

## Update Log

**2025-12-17:** Added gender feature and split functions up by their function.

**2025-12-16:** Initiated git repo.

**2025-12-14:** Started script in a scratch folder.
