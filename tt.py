from typing import Dict, Any, Callable
import ollama
from tools import validate_user,add_numbers, substract_numbers


query = 'add 1 + 2'
available_functions: Dict[str, Callable] = {}

response = ollama.chat(
    'llama3.2',
    messages=[{'role': 'user', 'content': query}],
    tools=[validate_user, add_numbers, substract_numbers]
)

def main():
    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            if function_to_call := available_functions.get(tool.function.name):
                print('Output', function_to_call(**tool.function_arguments))
            else:
                print('Not Found')

# Run the main loop
if __name__ == "__main__":
    main()