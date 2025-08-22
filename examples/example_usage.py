#!/usr/bin/env python3
"""
Example usage of Manager AI
Demonstrates various capabilities of the Manager AI system
"""

from langchain_core.messages import HumanMessage
from src.config.settings import setup_environment
from src.graph.manager_graph import ManagerAIGraph


def demo_profile_management():
    """Demonstrate user profile management."""
    print("\n" + "="*50)
    print("DEMO: User Profile Management")
    print("="*50)

    setup_environment()
    ai_graph = ManagerAIGraph()
    config = {"configurable": {"thread_id": "profile-demo", "user_id": "demo_user"}}

    interactions = [
        "My name is Alice Johnson, I'm a product manager in San Francisco.",
        "Actually, I should update that - I'm now working remotely from Seattle.",
    ]

    for interaction in interactions:
        print(f"\nUser: {interaction}")
        input_messages = [HumanMessage(content=interaction)]

        for chunk in ai_graph.stream({"messages": input_messages}, config, stream_mode="values"):
            latest_message = chunk["messages"][-1]
            if hasattr(latest_message, 'content') and latest_message.content:
                print(f"AI: {latest_message.content}")
                break


def demo_task_management():
    """Demonstrate task and ticket management."""
    print("\n" + "="*50)
    print("DEMO: Task Management")
    print("="*50)

    setup_environment()
    ai_graph = ManagerAIGraph()
    config = {"configurable": {"thread_id": "task-demo", "user_id": "task_user"}}

    interactions = [
        "Create a ticket to research competitor pricing strategies.",
        "Add another task to schedule quarterly team reviews.",
        "Show me my current ticket list.",
    ]

    for interaction in interactions:
        print(f"\nUser: {interaction}")
        input_messages = [HumanMessage(content=interaction)]

        for chunk in ai_graph.stream({"messages": input_messages}, config, stream_mode="values"):
            latest_message = chunk["messages"][-1]
            if hasattr(latest_message, 'content') and latest_message.content:
                print(f"AI: {latest_message.content}")
                break


def demo_research_capabilities():
    """Demonstrate research and information gathering."""
    print("\n" + "="*50)
    print("DEMO: Research Capabilities")
    print("="*50)

    setup_environment()
    ai_graph = ManagerAIGraph()
    config = {"configurable": {"thread_id": "research-demo", "user_id": "research_user"}}

    interactions = [
        "Find recent information about remote work productivity studies.",
        "Search for the latest trends in product management methodologies.",
    ]

    for interaction in interactions:
        print(f"\nUser: {interaction}")
        input_messages = [HumanMessage(content=interaction)]

        for chunk in ai_graph.stream({"messages": input_messages}, config, stream_mode="values"):
            latest_message = chunk["messages"][-1]
            if hasattr(latest_message, 'content') and latest_message.content:
                print(f"AI: {latest_message.content}")
                break


def run_all_demos():
    """Run all demonstration functions."""
    print("Manager AI - Demonstration Suite")
    print("=================================")

    try:
        demo_profile_management()
        demo_task_management() 
        demo_research_capabilities()

        print("\n" + "="*50)
        print("All demonstrations completed successfully!")
        print("="*50)

    except Exception as e:
        print(f"Error during demonstration: {e}")


if __name__ == "__main__":
    run_all_demos()
