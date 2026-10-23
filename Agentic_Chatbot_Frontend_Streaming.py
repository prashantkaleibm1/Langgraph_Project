from Agentic_Chatbot_Backend import chatbot
from langchain_core.messages import BaseMessage,HumanMessage
import streamlit as st

#CONFIG={'configurable' : {'thread_id': 'thread-1'}}
#thread_id="1"
#config= {'configurable' : {'thread_id' : thread_id}}

st.title("Agentic Chatbot with Langgraph")

if 'message_history' not in st.session_state :
    st.session_state['message_history'] =[]
    
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

    ## The following code is without streaming
    # Full content is received first before displaying
    #response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config=config)

    
    #ai_message = response["messages"][-1].content  # Full content is assigned to ai_message
    #with st.chat_message('assistant'):             # for displaying AI assistant icon
    #        st.text(ai_message)                    # Full content is displayed
    #### ............ Till here
    
    ## The following code is with streaming
    with st.chat_message('assistant'): 
        ai_message = st.write_stream(
         message_chunk.content for message_chunk, metadat in chatbot.stream(
             {'messages':[HumanMessage(content=user_input)]},
               config= {'configurable' : {'thread_id' : 'thread_1'}},
               stream_mode= 'messages'
               
             )   
        )
    #### ............ Till here
    
    # add message to the message history
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})

    

