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

1. Add more character attributes to the workflow.
2. Use sqlite to store characters.
3. Add a web form to make creating characters easier.
4. Replace the `get_country_choice` with a random picker from a list, but have an LLM generate the list.
5. Turn this into a serverless app.
6. Add documentation.
7. Add tests.

## Update Log

**2026-01-10:** Adhoc promting tests pass regularly.
Cleaning up, but still in progress.
Added `web.py` to start on the UI.

**2025-12-28:** Trying to build a chain of thought, but Llama still gets chatty with responses.

**2025-12-22:** Started working on the workflow, so users can start the character creation with a prompt.

**2025-12-17:** Added gender feature and split functions up by their function.

**2025-12-16:** Initiated git repo.

**2025-12-14:** Started script in a scratch folder.
