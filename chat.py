import ollama
from tools import add_posts,add_numbers, substract_numbers, general_query
import streamlit as st
from typing import Dict, Any, Callable


######### Terminal Verison ###### [Run !python3.12 chat.py]
# Main loop
# def main():
#     while True:
#         query = input("User (or type 'q', 'quit', or 'exit' to end): ")
#         if query.lower() in ['q', 'quit', 'exit']:
#             break
        
#         result = retrieval_chain.invoke({"input": query})
#         print("Assistant: ", result["answer"], "\n\n")

# # Run the main loop
# if __name__ == "__main__":
#     main()

# import time
# ######### UI Verison ###### [Run !python3.12 -m streamlit run chat.py]
# st.set_page_config(page_title="Document Co-Pilot")
# st.header("Document Co-Pilot")
# question =  st.text_input("Input", key="input")
# submit = st.button("Ask a question")
# if submit:
#     with st.spinner(":sunglasses: I'm on it, hold on a moment..."):
#         response = retrieval_chain.invoke({"input": question})
#         res=response['answer']
#     st.markdown(res)

######## Terminal Verison ###### [Run !python3.12 chat.py]
## Main loop
def main():
    while True:
        query = input("User (or type 'q', 'quit', or 'exit' to end): ")
        if query.lower() in ['q', 'quit', 'exit']:
            break

        available_functions: Dict[str, Callable] = {
            'add_posts': add_posts,
            'add_numbers': add_numbers,
            'substract_numbers': substract_numbers
        }
        print('***** Checking available tools')
        response = ollama.chat(
            'llama3.2',
            messages=[{'role': 'user', 'content': query}],
            tools=[add_posts, add_numbers, substract_numbers, general_query]
        )

        if response.message.tool_calls:
            for tool in response.message.tool_calls:
                if function_to_call := available_functions.get(tool.function.name):
                    print('Calling Tool:', tool.function.name)
                    print('Output', function_to_call(**tool.function.arguments))
                else:
                    print('No Tools Found, Activating RAG......')
                    print(general_query(query))

# Run the main loop
if __name__ == "__main__":
    main()
