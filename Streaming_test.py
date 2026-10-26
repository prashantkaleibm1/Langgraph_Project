from Agentic_Chatbot_Backend import chatbot
from langchain_core.messages import BaseMessage,HumanMessage


thread_id="1"
config= {'configurable' : {'thread_id':thread_id}}

#response = chatbot.invoke({ 'messages' :[HumanMessage(content="Generate a blog on AI")]},config)

#print(response["messages"][-1].content)

# Following code is for streaming output

for message_chunk,metadata in chatbot.stream({'messages':[HumanMessage(content="Generate a blog on AI")]},
               config= {'configurable' : {'thread_id' : 'thread_1'}},
               stream_mode= 'messages' ):
    if(message_chunk.content):
        print(message_chunk.content,end=" ",flush=True)
    
    


