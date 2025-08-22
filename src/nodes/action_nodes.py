from typing import List, Dict, Any
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import MessagesState
from langchain_groq import ChatGroq

from ..memory.memory_manager import load_memories
from ..models.schemas import UpdateMemory
from ..tools.search_tools import web_search, wiki_search, arxiv_search
from ..prompts.system_prompts import (
    DECIDE_ACTION_SYSTEM_PROMPT, 
    HANDLE_SEARCH_RESULT_SYSTEM_PROMPT
)


def decide_initial_action(state: MessagesState, config: RunnableConfig, store, model: ChatGroq):
    """Decides the initial action: search, update memory, or respond."""
    user_id = config["configurable"]["user_id"]
    mems = load_memories(user_id, store)

    system_msg_content = DECIDE_ACTION_SYSTEM_PROMPT.format(
        user_profile=mems["user_profile"] if mems["user_profile"] else "Not yet collected.",
        ticket=mems["ticket"] if mems["ticket"] else "No tickets yet.",
        instructions=mems["instructions"] if mems["instructions"] else "None specified.",
        userfeedback=mems["userfeedback"] if mems["userfeedback"] else "None yet.",
        productresearch=mems["productresearch"] if mems["productresearch"] else "None yet."
    )

    conversation_messages = [SystemMessage(content=system_msg_content)] + state["messages"]
    print("conversation_messages", conversation_messages)

    response = model.bind_tools(
        [UpdateMemory, web_search, wiki_search, arxiv_search],
    ).invoke(conversation_messages)

    print("response", response)
    return {"messages": [response]}


def handle_search_result(state: MessagesState, config: RunnableConfig, store, model: ChatGroq):
    """Processes search results and decides on next steps (e.g., update memory)."""
    user_id = config["configurable"]["user_id"]
    messages = state["messages"]

    # Find the AIMessage that initiated the tool calls
    last_ai_message_with_tool_calls = None
    for i in range(len(messages) - 1, -1, -1):
        if isinstance(messages[i], AIMessage) and messages[i].tool_calls:
            last_ai_message_with_tool_calls = messages[i]
            tool_messages_for_this_ai_call = [
                m for m in messages[i+1:] 
                if isinstance(m, ToolMessage) and m.tool_call_id in [tc['id'] for tc in last_ai_message_with_tool_calls.tool_calls]
            ]
            break

    if not last_ai_message_with_tool_calls or not tool_messages_for_this_ai_call:
        print("Error: Could not find corresponding AIMessage or ToolMessages for search results.")
        return {"messages": [AIMessage(content="Error: Could not properly process search tool results.")]}

    # Get the original user query that led to this AI decision
    original_user_query_message_content = "User query not easily found."
    for i in range(messages.index(last_ai_message_with_tool_calls) - 1, -1, -1):
        if isinstance(messages[i], HumanMessage):
            original_user_query_message_content = messages[i].content
            break

    # Consolidate search results
    all_search_results_content_parts = []
    original_query_context_parts = [f"User asked: '{original_user_query_message_content}'"]

    ai_decision_to_search_parts = []
    for tc in last_ai_message_with_tool_calls.tool_calls:
        tool_name = tc['name']
        tool_args = tc['args']
        ai_decision_to_search_parts.append(f"AI decided to use {tool_name} with args: {tool_args}")

    original_query_context_parts.append("\n".join(ai_decision_to_search_parts))
    original_query_context = "\n".join(original_query_context_parts)

    for tm in tool_messages_for_this_ai_call:
        if isinstance(tm.content, str) and tm.content.startswith("Error:"):
            all_search_results_content_parts.append(f"Error from tool {tm.name}: {tm.content}")
        elif isinstance(tm.content, dict):
            for key, value in tm.content.items():
                all_search_results_content_parts.append(f"Results from {tm.name} ({key}):\n{value}")
        else:
            all_search_results_content_parts.append(f"Content from tool {tm.name}: {str(tm.content)}")

    consolidated_search_results_content = "\n\n---\n\n".join(all_search_results_content_parts)

    # Prepare a limited history for the prompt
    history_for_prompt_idx = messages.index(last_ai_message_with_tool_calls)
    chat_history_summary = "\n".join([
        f"{m.type}: {str(m.content)[:200]}..." 
        for m in messages[max(0, history_for_prompt_idx-4):history_for_prompt_idx+1]
    ])

    system_msg_content = HANDLE_SEARCH_RESULT_SYSTEM_PROMPT.format(
        original_query_context=original_query_context,
        search_results_content=consolidated_search_results_content,
        chat_history=chat_history_summary
    )

    response = model.bind_tools([UpdateMemory]).invoke([
        SystemMessage(content=system_msg_content),
        HumanMessage(content=f"Search results received: {consolidated_search_results_content[:1000]}...")
    ])

    return {"messages": [response]}


def route_from_initial_action(state: MessagesState) -> str:
    """Routes from decide_initial_action node based on its tool call."""
    message = state['messages'][-1]
    if not message.tool_calls:
        return "END"

    tool_call = message.tool_calls[0]
    tool_name = tool_call['name']

    if tool_name == 'UpdateMemory':
        update_type = tool_call['args']['update_type']
        if update_type == 'user':
            return "update_userprofile"
        elif update_type == 'ticket':
            return "update_tickets"
        elif update_type == 'instructions':
            return "update_instructions"
        elif update_type == 'userfeedback':
            return "update_userfeedback"
        elif update_type == 'productresearch':
            return "update_productresearch"
        else:
            print(f"Warning: Unknown update_type '{update_type}' in route_from_initial_action")
            return "END"
    elif tool_name in ['web_search', 'wiki_search', 'arxiv_search']:
        return "execute_search_tools"
    else:
        print(f"Warning: Unknown tool '{tool_name}' in route_from_initial_action")
        return "END"


def route_from_search_handling(state: MessagesState) -> str:
    """Routes from handle_search_result node."""
    message = state['messages'][-1]
    if not message.tool_calls:
        return "END"

    tool_call = message.tool_calls[0]
    tool_name = tool_call['name']
    print("the tool which is called is", tool_name)

    if tool_name == 'UpdateMemory':
        update_type = tool_call['args']['update_type']
        if update_type == 'user':
            return "update_userprofile"
        elif update_type == 'ticket':
            return "update_tickets"
        elif update_type == 'instructions':
            return "update_instructions"
        elif update_type == 'userfeedback':
            return "update_userfeedback"
        elif update_type == 'productresearch':
            return "update_productresearch"
        else:
            print(f"Warning: Unknown update_type '{update_type}' in route_from_search_handling")
            return "END"
    else:
        print(f"Warning: Unexpected tool '{tool_name}' from handle_search_result")
        return "END"
