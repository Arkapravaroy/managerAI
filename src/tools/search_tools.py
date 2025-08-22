from typing import Dict, List, Any
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WikipediaLoader, ArxivLoader


@tool
def web_search(query: str) -> Dict[str, str]:
    """Search Tavily for a query and return maximum 3 results.

    Args:
        query: The search query.
    """
    tavily_tool = TavilySearchResults(max_results=3)
    # Invoke the Tavily tool correctly. It expects the query as the 'input'.
    search_results_list_of_dicts = tavily_tool.invoke(input=query)

    # Process the results (TavilySearchResults returns a list of dictionaries)
    formatted_search_docs_list = []
    if isinstance(search_results_list_of_dicts, list):
        for doc in search_results_list_of_dicts:
            source = doc.get("url", "N/A")
            content = doc.get("content", "")
            formatted_search_docs_list.append(
                f'\n{content}\n'
            )
    elif isinstance(search_results_list_of_dicts, str):
        formatted_search_docs_list.append(search_results_list_of_dicts)

    return {"web_results": "\n\n---\n\n".join(formatted_search_docs_list)}


@tool
def wiki_search(query: str) -> Dict[str, str]:
    """Search Wikipedia for a query and return maximum 2 results.

    Args:
        query: The search query.
    """
    search_docs: List[Any] = WikipediaLoader(query=query, load_max_docs=2).load()
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'\n{doc.page_content}\n'
            for doc in search_docs
        ])
    return {"wiki_results": formatted_search_docs}


@tool
def arxiv_search(query: str) -> Dict[str, str]:
    """Search Arxiv for a query and return maximum 3 result.

    Args:
        query: The search query.
    """
    search_docs: List[Any] = ArxivLoader(query=query, load_max_docs=3).load()
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'\n{doc.page_content[:2000]}\n'  # Increased snippet size
            for doc in search_docs
        ])
    return {"arxiv_results": formatted_search_docs}


# List of all search tools for easy import
search_execution_tools = [web_search, wiki_search, arxiv_search]
