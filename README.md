# llm-rpg-experiment

Contains an adapted version of code produced by Nemotron Ultra 253B, from the following prompt:

### Prompt 
I want to write Python code for a turn-based roleplaying experiment with LLMs. The idea is that one LLM acts as a player, who receives information about the game state and answers with the action that he is going to take for that turn. The other LLM acts as the game master, who responds to the players action with a description of the updated game state for the next turn.  
  
The default setting should be realistic and contemporary, with the player waking up in an unknown place, with no memory whatsoever.  
  
Please write the code, following these guidelines:  
- Use OpenAI-API compatible chat completion endpoints, with custom API URL, key and models. Use a configuration file, which can be specified per CLI argument.
- Write modular code with a clean main loop.
- Design adequate initial prompts for the default setting, but make the prompts configurable.
- Start with the gamemaster LLM and sent it the initial prompt, to let it describe the setting.. Then, send the response to the player LLM together with its respective initial prompt. Iterate from there.
- For the chat messages, make sure to assign the respectively other LLM the role "user", with the currently responding LLM acting as "assistant".
- The previous "chat" messages (with their roles respective to the current LLM) should of course always be included when calling the LLMs, such that they are aware of what happened in the previous turns. 
- Stream the LLM responses in real time.
- Make sure the output is sufficiently structured to be readable.

## Usage

Create a config file like the following:

```
api_url: "https://your-openai-api.com"
api_key: "YOUR_API_KEY"
gm_model: "Nemotron Ultra 253B"
player_model: "Nemotron Ultra 253B"
```

And start the run with `python rpg_experiment.py --config config.yaml`.

You may also set `gm_initial_prompt` and `player_initial_prompt` in your config to override the default prompts.
Note that these initial prompts are *not* employed as system prompts. For some LLMs it might be better to change the code and add them as system prompts.
