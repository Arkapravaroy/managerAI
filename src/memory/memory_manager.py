from typing import Dict, Any
from langgraph.store.base import BaseStore


def load_memories(user_id: str, store: BaseStore) -> Dict[str, Any]:
    """Helper to load all memories for a user."""
    memories = {
        "user_profile": None,
        "ticket": "",
        "instructions": "",
        "userfeedback": "",
        "productresearch": ""
    }

    profile_mem = store.search(("profile", user_id))
    if profile_mem:
        memories["user_profile"] = profile_mem[0].value

    ticket_mems = store.search(("ticket", user_id))
    # Tickets are stored as individual items, so we need to format them
    formatted_tickets = []
    for mem in ticket_mems:
        if isinstance(mem.value, dict):
            formatted_tickets.append(f"- Task: {mem.value.get('task', 'N/A')}, Status: {mem.value.get('status', 'N/A')}")
        elif isinstance(mem.value, str):
            formatted_tickets.append(mem.value)
    memories["ticket"] = "\n".join(formatted_tickets) if formatted_tickets else "No tickets yet."

    instr_mem = store.get(("instructions", user_id), "instructions")
    if instr_mem: 
        memories["instructions"] = instr_mem.value.get("memory", "")

    feedback_mem = store.get(("userfeedback", user_id), "userfeedback")
    if feedback_mem: 
        memories["userfeedback"] = feedback_mem.value.get("memory", "")

    research_mem = store.get(("productresearch", user_id), "productresearch")
    if research_mem: 
        memories["productresearch"] = research_mem.value.get("memory", "")

    return memories
