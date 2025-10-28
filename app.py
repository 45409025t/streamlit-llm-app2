import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.title("専門家チャットアプリ")
st.write(
    """
    異なる専門家としてAIが回答します。質問を入力し、専門家を選んでください 
    送信すると、選択した専門家の視点で回答します
    """
)

# --- LLM呼び出し関数 ---
def get_expert_response(user_input, expert_type):
    if expert_type == "医者":
        system_message = "あなたは優秀な医者です。医療に関する質問に丁寧に答えてください。"
    elif expert_type == "弁護士":
        system_message = "あなたは経験豊富な弁護士です。法律の観点から明確に回答してください。"
    else:
        system_message = "あなたは博識な専門家です。適切に回答してください。"

    chat = ChatOpenAI(temperature=0.2, openai_api_key=OPENAI_API_KEY)

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_message),
        HumanMessagePromptTemplate.from_template("{user_input}")
    ])

    messages = prompt.format_messages(user_input=user_input)
    response = chat.invoke(messages)

    return response.content

# --- UI 部分 ---
user_input = st.text_input("質問を入力してください:")
expert_type = st.radio("専門家の種類を選択してください:", ("医者", "弁護士"))

if st.button("送信"):
    if user_input:
        answer = get_expert_response(user_input, expert_type)
        st.write("### ▼回答")
        st.write(answer)
    else:
        st.warning("質問を入力してください")
