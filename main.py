from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streamlit import StreamlitCallbackHandler

import streamlit as st

from tool import TOOLS
from planner import Planner
from commander import Commander


# 下面這裏輸入你個人的 openai api key
API_KEY = ''

def chatbot_mode():
    st.title("Hi, I'm Document Agent!")

    parent_container = st.container()
    streamlit_callback = StreamlitCallbackHandler(parent_container=parent_container)

    agent = initialize_agent(
        tools=TOOLS,
        llm=ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=API_KEY, temperature=0),
        handle_parsing_errors=True,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        callbacks=[streamlit_callback],
    )

    planner = Planner(agent)

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hello"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(key="chat_input"):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        output = Commander({"api_key": API_KEY, "content": prompt}).start() # 處理用戶輸入

        response_list = planner.process_command(output)
        for step_msg in response_list:
            st.session_state.messages.append({"role": "assistant", "content": step_msg})
            st.chat_message("assistant").write(step_msg)

if __name__ == "__main__":
    chatbot_mode()
