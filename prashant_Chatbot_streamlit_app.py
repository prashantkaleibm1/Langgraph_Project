import os
from typing import TypedDict

import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Prashant Kale Details", page_icon="📄", layout="centered")
BASE_DIR = Path(__file__).parent
photo_path = BASE_DIR / "photo.jpg"

col1, col2 = st.columns([1, 6])

with col1:
    st.image(str(photo_path), width=70)

with col2:
    st.title("Ask about Prashant Kale")

#st.title("📄Ask about Prashant Kale ")
st.write("Ask questions about Prashant Kale's professional background.")

class LLMState(TypedDict):
    question: str
    answer: str

@st.cache_resource
def build_workflow():
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        api_key=OPENAI_API_KEY,
    )

    def llm_qa(state: LLMState) -> dict:
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.txt")
        with open(data_path, "r", encoding="utf-8") as file:
            file_content = file.read()

        prompt = f"""Answer the question using only the text below.
If the answer is not in the text, say it is unavailable.
Do not use outside knowledge.

Text:
{file_content}

Question: {state["question"]}

Answer:"""

        response = llm.invoke(prompt)
        return {"question": state["question"], "answer": response.content}

    graph = StateGraph(LLMState)
    graph.add_node("llm_qa", llm_qa)
    graph.add_edge(START, "llm_qa")
    graph.add_edge("llm_qa", END)
    return graph.compile()

question = st.text_input(
    "Enter your question",
    value="What are the previous companies of Prashant?",
)

if st.button("SUBMIT", type="primary", use_container_width=True):
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.txt")
    if not question.strip():
        st.warning("Please enter a question.")
    elif not os.path.isfile(data_path):
        st.error("data.txt was not found. Place it in the same folder as app.py.")
    else:
        try:
            with st.spinner("Executing LangGraph workflow..."):
                workflow = build_workflow()
                initial_state: LLMState = {
                    "question": question.strip(),
                    "answer": "",
                }
                final_state = workflow.invoke(initial_state)

            st.subheader("Answer")
            st.write(final_state["answer"])

            with st.expander("View final state"):
                st.json(final_state)

            with st.expander("View workflow graph"):
                st.graphviz_chart("""
                digraph {
                    rankdir=LR;
                    START -> llm_qa -> END;
                }
                """)
        except Exception as exc:
            st.error(f"Error executing workflow: {exc}")

st.caption("Answers are based only on data.txt. Keep your .env file private.")
