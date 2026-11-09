from Agentic_Chatbot_Backend_SQLite import chatbot ,get_all_threads
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
import streamlit as st
import random

# Write a function to create unique thread_id by random function
def generate_thread_id():
    return str(random.randint(0, 9999))  # Generate a random integer between 1000 and 9999 and convert it to a string
    
def add_thread(thread_id):
    # Prevent the same thread from being added multiple times
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)
        
def reset_chat():
    # Generate and assign a new thread ID
    st.session_state["thread_id"] = generate_thread_id()

    # Clear the current chat messages from the UI
    st.session_state["message_history"] = []

    # Add the new thread to the conversation list
    add_thread(st.session_state["thread_id"])   
    
# Load a previous conversation from the LangGraph checkpointer
def load_conversation(thread_id):

    # Get the saved state for the selected thread
    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )
    # Return saved messages
    # Return an empty list if no messages are available
    return state.values.get("messages", [])


# ========================= Sidebar threading feature =========================

st.title("Agentic Chatbot Langgraph_test")

# Create message history list when app runs for the first time
if 'message_history' not in st.session_state :
    st.session_state['message_history'] =[]
    
# Create a thread_id when app runs for the first time
if 'thread_id' not in st.session_state :
    st.session_state['thread_id'] =generate_thread_id()
    
# Get a list for  all conversation thread IDs
if "chat_threads" not in st.session_state:
    st.session_state['chat_threads'] = get_all_threads()
    
# Add the current thread to the conversation list
add_thread(st.session_state["thread_id"])
    
    
# Display the sidebar title
st.sidebar.title("My Conversations")


# Create a button for starting a new conversation
if st.sidebar.button("New Chat"):

    # Reset the current chat and create a new thread
    reset_chat()

    # Rerun the Streamlit app to update the interface
    st.rerun()

  
#display all conversation threads in reverse order
for thread_id in reversed(st.session_state['chat_threads']):
        if st.sidebar.button(f"Chat: {thread_id}"):
            st.session_state["thread_id"] = thread_id
        
            # Set the selected thread as the current thread
            st.session_state["thread_id"] = thread_id
    
            # Load the messages saved under the selected thread
            messages = load_conversation(thread_id)
    
        
    # Load the conversation from history when a thread is selected
    #messages = chatbot.get_state(   
    #        config={
    #            "configurable": {
    #                "thread_id": thread_id
    #            }
    #        }
    #    ).values.get("messages", [])    
    #    
        
            # Temporary list for converting LangChain messages
            # into Streamlit's required message format
            temp_messages = []
    
    
            # Loop through all saved messages
            for message in messages:
    
                # Check whether the message was sent by the user
                if isinstance(message, HumanMessage):
                    role = "user"
    
                # Check whether the message was sent by the AI
                elif isinstance(message, AIMessage):
                    role = "assistant"
    
                # Ignore other message types, such as ToolMessage
                else:
                    continue
    
    
                # Convert the LangChain message into a dictionary
                temp_messages.append({
                    "role": role,
                    "content": message.content
                })
    
    
            # Replace the current UI history with the selected conversation
            st.session_state["message_history"] = temp_messages
    
            # Rerun the application to display the loaded messages
            st.rerun()
    
        
           
#Loading the conversation from history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input=st.chat_input('Type Here')

# Invoke the chatbot only after the user submits a message
if user_input:
    # add message to the message history
    st.session_state['message_history'].append({
        'role':'user','content':user_input})
    
# Display the user message in the chat interface        
    with st.chat_message('user'):  # for displaying user icon
           st.text(user_input)

# Pass the current thread_id to LangGraph to maintain the conversation context
    CONFIG = {'configurable' : {'thread_id': st.session_state["thread_id"]}}

    #message= {'messages': [HumanMessage(content="Generate Blog in USA Midterm poll")      
    #                       ]}

    # Replace the above message with the user input
    # Create the assistant message using the user input and pass it to the chatbot for processing
    message= {'messages': [HumanMessage(content=user_input)     
                     ]}
    with st.chat_message('assistant'): 
        ai_message = st.write_stream(
         message_chunk.content for message_chunk, metadata 
         in chatbot.stream(
               message,
               CONFIG,
               stream_mode= 'messages'
               
             )   
         # Dispaly only AI messages
         if isinstance(message_chunk, AIMessage) 
        )

    # add message to the message history
    st.session_state['message_history'].append({
        'role':'assistant','content':ai_message})
    
    #response = chatbot.invoke(message,config=CONFIG)

    #response=chatbot.stream(message,config=CONFIG,stream_mode='messages')

    #print(response) # This gives generator object, 
            #you can iterate over it to get the messages in real-time

    #for message_chunk, metadata in response:
    #    if message_chunk.content:
    #        print(message_chunk.content,end='',flush=True)  
        # This will print the content of each message chunk as 
        # it is received




    #print(response['messages'][0].content)
    #print(response['messages'][-1].content)