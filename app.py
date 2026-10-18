# %%
# Imports
import os
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import TypedDict

# %%
# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

# %%
# Define LLM
llm=ChatOpenAI(model_name="gpt-3.5-turbo",
                 temperature=0,
                 api_key=OPENAI_API_KEY)

# %%
# Define State
class LLMState(TypedDict):
    question: str
    answer: str

# %%
# Node: Read text file and answer the question
def llm_qa(state: LLMState) -> dict:
    with open("data.txt", "r", encoding="utf-8") as file:
        file_content = file.read()

    prompt = f"""
    Answer the question using only the text below.
    If the answer is not in the text, say it is unavailable.

    Text:
    {file_content}

    Question: {state["question"]}
    """

    response = llm.invoke(prompt)

    return {
        "question": state["question"],
        "answer": response.content
    }


# %%
# Define and compile graph
graph = StateGraph(LLMState)

# Add nodes to the graph
graph.add_node('llm_qa', llm_qa)


# %%
# add edges to the graph
graph.add_edge(START, 'llm_qa')
graph.add_edge('llm_qa', END)

# %%
#compile the graph
workflow=graph.compile()

# %%
# Execute Graph
initial_state = LLMState(question="What are the previous companies of Prashant?")
final_state = workflow.invoke(initial_state)
print(final_state)


# %%
#vizualize the graph
from IPython.display import Image
Image(workflow.get_graph().draw_mermaid_png())



