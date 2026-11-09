# Imports
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage,HumanMessage
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
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
        
        
# Persistence property (Sqlite database) in Chatbot
conn=sqlite3.connect('chatbot.db',check_same_thread=False)
checkpoint= SqliteSaver(conn)


graph=StateGraph(ChatState)

# Add node
graph.add_node('chat_node',chat_node)

# Add edges
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot=graph.compile(checkpointer=checkpoint)


def get_all_threads():
    # Lists all chekpoints in the database
    threads=checkpoint.list(None)

    all_threads=set()    # set  data sructure in python only has unique valuse

    for thread in threads:
         all_threads.add(thread.config['configurable']['thread_id'])

     # Prints only unique thread IDs in the database in list format
    return list(all_threads)



# thread_id="default_thread"
# config= {'configurable' : {'thread_id':thread_id}}
# initial_state = { 'messages' :[HumanMessage(content="Hello, My name is Prashant")]}
# response = chatbot.invoke(initial_state,config)

# print(response['messages'][0].content)

# print(response['messages'][-1].content)

