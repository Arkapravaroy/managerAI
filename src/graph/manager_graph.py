from langchain_groq import ChatGroq
from trustcall import create_extractor
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.store.memory import InMemoryStore

from ..config.settings import MODEL_NAME, MODEL_TEMPERATURE
from ..models.schemas import Profile, TicketDetails, UpdateMemory
from ..tools.search_tools import search_execution_tools
from ..nodes.action_nodes import (
    decide_initial_action, 
    handle_search_result,
    route_from_initial_action,
    route_from_search_handling
)
from ..nodes.update_nodes import (
    update_userprofile,
    update_tickets,
    update_instructions,
    update_userfeedback,
    update_productresearch
)


class ManagerAIGraph:
    def __init__(self):
        self.model = ChatGroq(model=MODEL_NAME, temperature=MODEL_TEMPERATURE)
        self.across_thread_memory = InMemoryStore()
        self.within_thread_memory = MemorySaver()

        # Create extractors
        self.profile_extractor = create_extractor(
            self.model,
            tools=[Profile],
            tool_choice="Profile",
        )

        self.ticket_extractor = create_extractor(
            self.model,
            tools=[TicketDetails],
            tool_choice="TicketDetails",
            enable_inserts=True
        )

        self.search_tool_node = ToolNode(search_execution_tools)
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the state graph with all nodes and edges."""
        builder = StateGraph(MessagesState)

        # Create node wrapper functions
        def decide_initial_action_node(state, config):
            return decide_initial_action(state, config, self.across_thread_memory, self.model)

        def handle_search_result_node(state, config):
            return handle_search_result(state, config, self.across_thread_memory, self.model)

        def update_userprofile_node(state, config):
            return update_userprofile(state, config, self.across_thread_memory, self.profile_extractor)

        def update_tickets_node(state, config):
            return update_tickets(state, config, self.across_thread_memory, self.ticket_extractor)

        def update_instructions_node(state, config):
            return update_instructions(state, config, self.across_thread_memory, self.model)

        def update_userfeedback_node(state, config):
            return update_userfeedback(state, config, self.across_thread_memory, self.model)

        def update_productresearch_node(state, config):
            return update_productresearch(state, config, self.across_thread_memory, self.model)

        # Add nodes
        builder.add_node("decide_initial_action", decide_initial_action_node)
        builder.add_node("handle_search_result", handle_search_result_node)
        builder.add_node("update_userprofile", update_userprofile_node)
        builder.add_node("update_tickets", update_tickets_node)
        builder.add_node("update_instructions", update_instructions_node)
        builder.add_node("update_userfeedback", update_userfeedback_node)
        builder.add_node("update_productresearch", update_productresearch_node)
        builder.add_node("execute_search_tools", self.search_tool_node)

        # Define edges
        builder.add_edge(START, "decide_initial_action")

        builder.add_conditional_edges(
            "decide_initial_action",
            route_from_initial_action,
            {
                "execute_search_tools": "execute_search_tools",
                "update_userprofile": "update_userprofile",
                "update_tickets": "update_tickets",
                "update_instructions": "update_instructions",
                "update_userfeedback": "update_userfeedback",
                "update_productresearch": "update_productresearch",
                END: END
            }
        )

        builder.add_conditional_edges(
            "handle_search_result",
            route_from_search_handling,
            {
                "update_userprofile": "update_userprofile",
                "update_tickets": "update_tickets",
                "update_instructions": "update_instructions",
                "update_userfeedback": "update_userfeedback",
                "update_productresearch": "update_productresearch",
                END: END
            }
        )

        # Edges from update nodes: loop back to decide_initial_action
        builder.add_edge("update_userprofile", "decide_initial_action")
        builder.add_edge("update_tickets", "decide_initial_action")
        builder.add_edge("update_instructions", "decide_initial_action")
        builder.add_edge("update_userfeedback", "decide_initial_action")
        builder.add_edge("update_productresearch", "decide_initial_action")
        builder.add_edge("execute_search_tools", "handle_search_result")

        return builder.compile(checkpointer=self.within_thread_memory, store=self.across_thread_memory)

    def stream(self, input_data, config, stream_mode="values"):
        """Stream the graph execution."""
        return self.graph.stream(input_data, config, stream_mode=stream_mode)

    def invoke(self, input_data, config):
        """Invoke the graph once."""
        return self.graph.invoke(input_data, config)
