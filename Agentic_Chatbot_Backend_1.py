from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


# Load environment variables from .env (including OPENAI_API_KEY).
load_dotenv()

# Initialize the chat model instance. Do not assign llm = ChatOpenAI
# without parentheses, because that assigns the class rather than an instance.
llm = ChatOpenAI(model="gpt-4o-mini")


class ChatState(TypedDict):
    # add_messages appends each node's response to the conversation history.
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState) -> dict:
    """Generate an assistant response from the current conversation history."""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


def build_chatbot():
    """Build a chatbot graph with in-memory conversation checkpointing."""
    graph = StateGraph(ChatState)
    graph.add_node("chat_node", chat_node)
    graph.add_edge(START, "chat_node")
    graph.add_edge("chat_node", END)

    # MemorySaver preserves state between calls in this running process.
    return graph.compile(checkpointer=MemorySaver())


def main() -> None:
    chatbot = build_chatbot()
    thread_id = "1"
    config = {"configurable": {"thread_id": thread_id}}

    print("LangGraph chatbot started. Type 'exit' or 'quit' to stop.")
    while True:
        try:
            user_text = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if user_text.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break
        if not user_text:
            continue

        try:
            result = chatbot.invoke(
                {"messages": [HumanMessage(content=user_text)]},
                config=config,
            )
            print("\nAssistant:", result["messages"][-1].content)
        except Exception as exc:
            print(f"\nError while invoking the chatbot: {exc}")
            print(
                "Check that OPENAI_API_KEY is set correctly in your .env file "
                "and that the required packages are installed."
            )


if __name__ == "__main__":
    main()
