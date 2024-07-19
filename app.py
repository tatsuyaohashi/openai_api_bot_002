pip install -r requirements.txt

import streamlit as st
import openai

# StreamlitのSecretsからOpenAI APIキーを取得
openai.api_key = st.secrets["OpenAIAPI"]["openai_api_key"]

# st.session_stateにメッセージの履歴を保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
    ]

# チャットのやり取りを処理する関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄をクリア

# ユーザーインターフェースの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に表示
        speaker = "🙂"
        if message["role"] == "assistant":
            speaker = "🤖"

        st.write(f"{speaker}: {message['content']}")
