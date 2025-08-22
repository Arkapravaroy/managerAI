import uuid
from datetime import datetime
from typing import Literal
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, merge_message_runs
from langgraph.graph import MessagesState
from langchain_groq import ChatGroq

from ..models.schemas import Profile, TicketDetails
from ..prompts.system_prompts import (
    TRUSTCALL_INSTRUCTION,
    CREATE_INSTRUCTIONS_PROMPT,
    UPDATE_PRODUCT_RESEARCH_PROMPT,
    USER_FEEDBACK_PROMPT
)


def update_userprofile(state: MessagesState, config: RunnableConfig, store, profile_extractor):
    user_id = config["configurable"]["user_id"]
    namespace = ("profile", user_id)

    messages_for_extraction = [m for m in state["messages"] if not isinstance(m, ToolMessage)]

    trustcall_input_messages = list(merge_message_runs(
        messages=[SystemMessage(content=TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat()))] +
        messages_for_extraction
    ))

    existing_items = store.search(namespace)
    existing_memories = ([(existing_item.key, "Profile", existing_item.value)
                         for existing_item in existing_items]
                        if existing_items else None)

    result = profile_extractor.invoke({
        "messages": trustcall_input_messages,
        "existing": existing_memories
    })

    tool_call_id = state["messages"][-1].tool_calls[0]['id']

    if result["responses"]:
        profile_data = result["responses"][0]
        store.put(namespace, "user_profile_doc", profile_data)
        confirmation_msg = f"User profile updated. Current profile details: {profile_data.model_dump_json(indent=2)}"
        return {"messages": [ToolMessage(content=confirmation_msg, tool_call_id=tool_call_id)]}
    else:
        return {"messages": [ToolMessage(content="No profile information extracted to update.", tool_call_id=tool_call_id)]}


def update_tickets(state: MessagesState, config: RunnableConfig, store, ticket_extractor):
    user_id = config["configurable"]["user_id"]
    namespace = ("ticket", user_id)

    messages_for_extraction = [m for m in state["messages"] if not isinstance(m, ToolMessage)]

    trustcall_input_messages = list(merge_message_runs(
        messages=[SystemMessage(content=TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat()))] +
        messages_for_extraction
    ))

    existing_items = store.search(namespace)
    existing_memories = ([(existing_item.key, "TicketDetails", existing_item.value)
                         for existing_item in existing_items]
                        if existing_items else None)

    result = ticket_extractor.invoke({
        "messages": trustcall_input_messages,
        "existing": existing_memories
    })

    tool_call_id = state["messages"][-1].tool_calls[0]['id']

    if result["responses"]:
        updated_ticket_details_for_user = []
        for r_meta, ticket_obj in zip(result["response_metadata"], result["responses"]):
            ticket_id = r_meta.get("json_doc_id", str(uuid.uuid4()))
            store.put(namespace, ticket_id, ticket_obj.model_dump())
            detail_str = (
                f" - Task: {ticket_obj.task}\n"
                f" Status: {ticket_obj.status}\n"
                f" Time to complete: {ticket_obj.time_to_complete or 'N/A'} minutes\n"
                f" Deadline: {ticket_obj.deadline.isoformat() if ticket_obj.deadline else 'N/A'}\n"
                f" Solutions: {', '.join(ticket_obj.solutions) if ticket_obj.solutions else 'None listed'}"
            )
            updated_ticket_details_for_user.append(detail_str)

        confirmation_msg = "Ticket(s) processed. Details:\n" + "\n".join(updated_ticket_details_for_user)
        return {"messages": [ToolMessage(content=confirmation_msg, tool_call_id=tool_call_id)]}
    else:
        return {"messages": [ToolMessage(content="No new ticket information was extracted to update/create.", tool_call_id=tool_call_id)]}


def update_generic_memory(
    state: MessagesState,
    config: RunnableConfig,
    store,
    model: ChatGroq,
    memory_type: Literal['instructions', 'userfeedback', 'productresearch'],
    prompt_template: str
):
    user_id = config["configurable"]["user_id"]
    namespace = (memory_type, user_id)
    key = memory_type

    current_memory_doc = store.get(namespace, key)
    current_memory_content = current_memory_doc.value.get("memory", "") if current_memory_doc else ""

    relevant_history = state["messages"][-5:-1]
    formatted_history = "\n".join([f"{m.type}: {m.content}" for m in relevant_history])

    if memory_type == "instructions":
        system_msg_content = prompt_template.format(
            current_instructions=current_memory_content,
            relevant_user_input=formatted_history
        )
    elif memory_type == "productresearch":
        system_msg_content = prompt_template.format(
            current_productresearch=current_memory_content,
            relevant_inputs=formatted_history
        )
    else:  # userfeedback
        system_msg_content = prompt_template.format(
            current_feedback=current_memory_content,
            relevant_user_input=formatted_history
        )

    new_memory_response = model.invoke([
        SystemMessage(content=system_msg_content),
        HumanMessage(content="Please generate the updated content based on the provided information.")
    ])
    new_memory_content = new_memory_response.content

    store.put(namespace, key, {"memory": new_memory_content})

    tool_call_id = state["messages"][-1].tool_calls[0]['id']
    confirmation_msg = f"{memory_type.capitalize()} memory has been updated. New content:\n---\n{new_memory_content}\n---"
    return {"messages": [ToolMessage(content=confirmation_msg, tool_call_id=tool_call_id)]}


def update_instructions(state: MessagesState, config: RunnableConfig, store, model: ChatGroq):
    return update_generic_memory(state, config, store, model, "instructions", CREATE_INSTRUCTIONS_PROMPT)


def update_userfeedback(state: MessagesState, config: RunnableConfig, store, model: ChatGroq):
    return update_generic_memory(state, config, store, model, "userfeedback", USER_FEEDBACK_PROMPT)


def update_productresearch(state: MessagesState, config: RunnableConfig, store, model: ChatGroq):
    return update_generic_memory(state, config, store, model, "productresearch", UPDATE_PRODUCT_RESEARCH_PROMPT)
