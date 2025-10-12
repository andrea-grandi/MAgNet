from magnet.nets.qa_specialized_net.agent.swarms import app
from langchain_core.globals import set_debug, set_verbose

# Abilita debug verboso per vedere tutti i passaggi
set_debug(True)
set_verbose(True)

config = {"configurable": {"thread_id": "1"}}

# Main interaction loop
while True:
    user_input = input("\nEnter your request (or 'exit' to quit): ")

    if user_input.lower() == 'exit':
        print("Goodbye!")
        break

    result = app.invoke(
        {"messages": [{
            "role": "user",
            "content": user_input
        }]},
        config, #type: ignore
    )

    # Display the response
    for m in result["messages"]:
        print(m.pretty_print())