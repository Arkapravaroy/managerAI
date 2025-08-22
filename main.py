#!/usr/bin/env python3
"""
Manager AI - Intelligent Assistant for CEOs, Product Managers, and Executive Managers
A conversational AI agent that helps with project management, research, and task tracking.
"""

from langchain_core.messages import HumanMessage
from src.config.settings import setup_environment
from src.graph.manager_graph import ManagerAIGraph


def main():
    """Main function to run the Manager AI."""
    print("Initializing Manager AI...")

    # Setup environment variables
    setup_environment()

    # Initialize the graph
    ai_graph = ManagerAIGraph()

    print("Manager AI initialized successfully!")
    print("\n" + "="*50)
    print("Manager AI - Ready to assist!")
    print("="*50)
    print("\nType 'quit' or 'exit' to end the session.")
    print("Type 'help' for usage examples.\n")

    # Configuration for the session
    config = {"configurable": {"thread_id": "main-session", "user_id": "user1"}}

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Thank you for using Manager AI. Goodbye!")
                break

            if user_input.lower() == 'help':
                show_help()
                continue

            if not user_input:
                continue

            # Process the user input
            input_messages = [HumanMessage(content=user_input)]

            print("\nManager AI: ", end="")
            for chunk in ai_graph.stream({"messages": input_messages}, config, stream_mode="values"):
                latest_message = chunk["messages"][-1]
                # Only print AI messages to avoid showing tool calls
                if hasattr(latest_message, 'content') and latest_message.content and not hasattr(latest_message, 'tool_calls'):
                    print(latest_message.content)
                    break

            print("\n" + "-"*50 + "\n")

        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.\n")


def show_help():
    """Display help information."""
    help_text = """
Manager AI Help
===============

Example commands you can try:

1. Personal Information:
   - "My name is John and I work for the engineering team in New York."
   - "I'm a product manager at TechCorp."

2. Task Management:
   - "Please create a ticket to investigate new CRM options."
   - "Add a task to review quarterly performance metrics."
   - "Show me my current tickets."

3. Research & Information:
   - "Can you find recent articles about AI in project management?"
   - "Search for information about agile methodologies."
   - "What are the latest trends in product management?"

4. Memory Management:
   - "Update my research notes with findings about competitor analysis."
   - "Add feedback that users want better mobile experience."
   - "Set my preference to always include deadlines in tickets."

The AI will remember your information and preferences across the session.
    """
    print(help_text)


def run_example():
    """Run a simple example interaction."""
    print("\n" + "="*50)
    print("Running Example Interaction")
    print("="*50)

    setup_environment()
    ai_graph = ManagerAIGraph()

    config = {"configurable": {"thread_id": "example-session", "user_id": "example_user"}}

    # Example interactions
    examples = [
        "My name is Sarah, and I work for the product team in London.",
        "Please create a ticket to investigate new CRM options.",
        "Can you find recent articles on AI in project management?"
    ]

    for example in examples:
        print(f"\nUser: {example}")
        print("Manager AI: ", end="")

        input_messages = [HumanMessage(content=example)]
        for chunk in ai_graph.stream({"messages": input_messages}, config, stream_mode="values"):
            latest_message = chunk["messages"][-1]
            if hasattr(latest_message, 'content') and latest_message.content and not hasattr(latest_message, 'tool_calls'):
                print(latest_message.content)
                break

        print("\n" + "-"*30)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        run_example()
    else:
        main()
