from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import streamlit as st

load_dotenv()

# LangChainを使ってLLMにプロンプトを渡して回答を得る機能
# 引数：system_message（システムメッセージ）、user_message（ユーザーメッセージ）
# 戻り値：LLMの応答
# 備考：OpenAIのAPIキーは環境変数から取得されることを前提としています。
def get_llm_response(system_message, user_message):
    try:
        llm = OpenAI(temperature=0.7)
        prompt = PromptTemplate(
            input_variables=["system_message", "user_message"],
            template="{system_message}\n\n{user_message}"
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.run(system_message=system_message, user_message=user_message)
        return response
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

def main():
    st.set_page_config(page_title="【提出課題】LLM機能を搭載したWebアプリ", layout="wide")

    # StreamlitのUI設定
    st.write("##### 相談分野のLLM専門家が質問に回答します。")
    st.write("入力フォームに相談事項を入力し、「相談」ボタンを押すことで回答が得られます。")
    selected_item = st.radio(
        "相談分野を選択してください。",
        ["健康", "キャリア"]
    )

    # ユーザーからの入力を受け取る
    input_message = st.text_input("相談内容を入力してください。", placeholder="ここに相談内容を入力してください。")

    st.divider()

    if st.button("相談"):
        if not input_message.strip():
            st.warning("相談内容を入力してください。")
        else:
            if selected_item == "健康":
                system_message = "あなたは健康に関する専門カウンセラーです。"
            else:
                system_message = "あなたはキャリアに関する専門カウンセラーです。"
            response = get_llm_response(system_message, input_message)
            st.write("### 回答:")
            st.write(response)

main()