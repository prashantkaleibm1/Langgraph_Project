from Agentic_Chatbot_Backend import chatbot
from langchain_core.messages import BaseMessage,HumanMessage
import streamlit as st
import uuid     # To Generate Unique ID for thread

# Function to generate unique Thread ID for each conversation

def generate_thread_id():
    return str(uuid.uuid4())

# Add a new tread ID to the conversation list
def add_thread(thread_id):
    #prevent same thread ID to get added multiple times
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)
        
def reset_chat():
    # Generate and assign a new thread_id
    st.session_state["thread_id"] = generate_thread_id()
    
    #Clear the current chat message from the UI
    st.session_state['message_history'] =[]
    
    # Add new thread to the conversation list
    add_thread(st.session_state["thread_id"])
    
def load_conversation(thread_id):
    # Get the saved state for the selected thread
    state = chatbot.get_state(
        config= {
            "configurable" : {
                "thread_id" : thread_id
            }
        }
        
    )    
    
    # Return saved messages
    # Return empty list if no messages are available
    return state.values.get("messages",[])


#CONFIG={'configurable' : {'thread_id': 'thread-1'}}
#thread_id="1"
#config= {'configurable' : {'thread_id' : thread_id}}

st.title("Agentic Chatbot with Langgraph")

# Create message history list when app runs for the first time
if 'message_history' not in st.session_state :
    st.session_state['message_history'] =[]
    
# Create a thread_id when app runs for the first time
if 'thread_id' not in st.session_state :
    st.session_state['thread_id'] =[]
    
    
# Create a list for storing all conversation thread IDs
if "chat_threads" not in st.session_state:
    st.session_state['chat_threads'] =[]
    
  
    
    
# Display the sidebar Title
st.sidebar.title("My Conversation threads")    
# Create a Button for starting a new Conversation
if st.sidebar.button("New Chat"):
    
    # Reset a current chat and create new thread
    reset_chat()
    
    # Rerun the streamlit app to update the interface
    st.experimental_rerun()
    
# Dispalys all conversation threads in reverse order
# This shows newest conversation first
for thread_id in st.session_state["chat_threads"][::-1] :
    
    # Create one sidebar button for every conversation
    if st.sidebar.button(str(thread_id),key=thread_id):  
         
        # Set the selected thread as the current thread
        st.session_state["thread_id"] = thread_id
        
        # Load the message saved under selected thread
        messages=load_conversation(thread_id)          # Loads all previous conversations
        


# Loading the conversation threads from history

#for thread in st.session_state['message_history']:
#   with st.chat_message(thread['role']):
#        st.text(thread['content'])
  
      
    
# Loading the conversation from history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
    


user_input=st.chat_input('Type Here')

# Invoke the chatbot only after the user submits a message
if user_input:
    # add message to the message history
    st.session_state['message_history'].append({'role':'user','content':user_input})
    
        
    with st.chat_message('user'):  # for displaying user icon
           st.text(user_input)
           
# Pass current thread_id to the LangGraph
# LangGraph will save and retrieve the conversation history using the thread_id
    config= {'configurable' : {'thread_id' : st.session_state['thread_id']
                               }
             }

    response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config=config)

    ai_message = response["messages"][-1].content
    # add message to the message history
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})

    with st.chat_message('assistant'):   # for displaying AI assistant icon
        st.text(ai_message)

