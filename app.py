import openai
# import toml
import streamlit as st


def show_messages(text):
    messages_str = [
        f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][1:]
    ]
    text.text_area("Messages", value=str("\n".join(messages_str)), height=400)


# with open("secrets.toml", "r") as f:
#     config = toml.load(f)
OPENAI_KEY = st.secrets["OPENAI_KEY"]

openai.api_key = OPENAI_KEY
BASE_PROMPT = [{"role": "简历代写师", "content": ''' ## Goals:
- 根据用户提供的岗位title或岗位描述，向用户提问以挖掘用户的优势、职业经历
- 深挖追问问题，直到用户的回答足以让你为其写一份漂亮的简历
- 最终给用户输出一份包含个人介绍、工作经历、项目经历三段内容的完整文本

## Skills:
- 在个人优势、工作经历、项目经历方面提出好的问题，挖掘用户的闪光点
- 熟练各种简历书写的方法论，比如STAR法则，量化成果原则等
- 一次提出一个问题，等用户回答完毕后再提出下一个问题

## Workflows:
1. 初始化：欢迎用户，并介绍自己的能力和工作流程。
2. 向用户提问：问题能够启发用户思考并表达自己的优势、讲述自己的工作经历，一次提出一个问题
3. 处理用户输入：根据用户的所有回复，总结个人介绍、工作经历、项目经历三段内容
4. 输出结果：将生成的个人介绍、工作经历、项目经历三段内容展示给用户'''}]

if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT

st.header("ChatGPT对话辅助工具")

text = st.empty()
show_messages(text)

prompt = st.text_input("Prompt", value="Enter your message here...")

if st.button("Send",type="primary"):
    with st.spinner("Generating response..."):
        st.session_state["messages"] += [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301", messages=st.session_state["messages"]
        )
        message_response = response["choices"][0]["message"]["content"]
        role_response = response["choices"][0]["message"]["role"]
        st.session_state["messages"] += [
            {"role": role_response, "content": message_response}
        ]
        show_messages(text)

if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)
