import os
import argparse
import yaml
import openai
from typing import List, Dict

def load_config(config_path: str) -> Dict:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Set default initial prompts if not provided in config
    if 'gm_initial_prompt' not in config:
        config['gm_initial_prompt'] = """
You are the Game Master. The player has just awoken in an unknown contemporary setting with no memory.
Describe the initial scene in a realistic and immersive way. Keep your descriptions concise but vivid.
The player's actions will be provided as user messages. Respond with the updated game state after each action,
guiding the narrative forward. When you deem the story as concluded, you may end the game by stating **GAME OVER**.
"""
    if 'player_initial_prompt' not in config:
        config['player_initial_prompt'] = """
You are the player. You have just awoken in an unknown contemporary setting with no memory.
The Game Master will describe the scene. Respond with your next action, focusing on realistic decisions and
interactions. The Game Master's messages are the user's input. Provide your action in the form of a short
sentence or phrase.
"""
    return config

def call_llm(config: Dict, llm_type: str, messages: List[Dict]) -> str:
    model = config[f'{llm_type}_model']
    openai.api_key = config['api_key']
    os.environ["OPENAI_BASE_URL"] = config['api_url']

    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )

    response_text = []
    print()
    print(f"{'**GM**' if llm_type == 'gm' else '**Player**'}: ", end='')
    for chunk in response:
        if chunk.choices and len(chunk.choices) > 0:
            text = chunk.choices[0].delta.content
            if text:
                response_text.append(text)
                print(text, end='', flush=True)
    full_response = ''.join(response_text).strip()
    print()  # Move to new line after response
    return full_response

def build_api_messages(history: List[Dict], current_llm: str, config: Dict) -> List[Dict]:
    initial_prompt = config[f'{current_llm}_initial_prompt']
    if current_llm == "player":
        messages = [{"role": "user", "content": f"{initial_prompt}\n {history[0]['content']}"}]
        it_start = 1
    else:
        messages = [{"role": "user", "content": initial_prompt}]
        it_start = 0
    for msg in history[it_start:]:
        if msg['sender'] == current_llm:
            role = "assistant"
        else:
            role = "user"
        messages.append({"role": role, "content": msg['content']})
    return messages

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True, help='Path to YAML config file')
    args = parser.parse_args()

    config = load_config(args.config)
    history = []

    # Initial Game Master prompt
    gm_messages = build_api_messages(history, 'gm', config)
    gm_response = call_llm(config, 'gm', gm_messages)
    history.append({'sender': 'gm', 'content': gm_response})

    # Initial Player prompt
    player_messages = build_api_messages(history, 'player', config)
    player_response = call_llm(config, 'player', player_messages)
    history.append({'sender': 'player', 'content': player_response})

    # Main game loop
    while True:
        # Game Master's turn
        gm_messages = build_api_messages(history, 'gm', config)
        gm_response = call_llm(config, 'gm', gm_messages)
        if 'GAME OVER' in gm_response:
            break
        history.append({'sender': 'gm', 'content': gm_response})

        # Player's turn
        player_messages = build_api_messages(history, 'player', config)
        player_response = call_llm(config, 'player', player_messages)
        history.append({'sender': 'player', 'content': player_response})

if __name__ == '__main__':
    main()
