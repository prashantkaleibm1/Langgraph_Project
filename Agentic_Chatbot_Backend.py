# Imports
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage,HumanMessage
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages

load_dotenv()

llm=ChatOpenAI(model="gpt-4o-mini")

# Define the state

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]
    
    
def chat_node(state: ChatState):
    #Take user query from the state
    messages=state['messages']
    response = llm.invoke(messages)
    return {'messages' :[response]}  # response stored in messages which is itself a list
        
        
# Persistence property (memory) in Chatbot

checkpoint= MemorySaver()
graph=StateGraph(ChatState)

# Add node
graph.add_node('chat_node',chat_node)

# Add edges
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot=graph.compile(checkpointer=checkpoint)

thread_id="1"
config= {'configurable' : {'thread_id':thread_id}}
initial_state = { 'messages' :[HumanMessage(content="Hello")]}
response = chatbot.invoke(initial_state,config)

