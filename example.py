import csv
import pandas as pd
import streamlit as st
from streamlit_chatbox import *
import time
import simplejson as json
import re


from streamlit_chatbox.storydata import StoryData

chat_box = ChatBox()
chat_box.use_chat_name("chat1") # add a chat conversatoin

chat_box.init_session()
chat_box.output_messages()
if 'story_data' not in st.session_state:
    st.session_state.story_data = None
    
if 'session' not in st.session_state:
    st.session_state.session = False


if 'now_idx_dialogue' not in st.session_state:
    st.session_state.now_idx_dialogue = 0
if 'now_dialogue' not in st.session_state:
    st.session_state.now_dialogue = []
if 'now_movement' not in st.session_state:
    st.session_state.now_movement = []
if 'now_sound_emotion' not in st.session_state:
    st.session_state.now_sound_emotion = []
if 'now_movement_sound' not in st.session_state:
    st.session_state.now_movement_sound = []
if 'next_dialogue' not in st.session_state:
    st.session_state.next_dialogue = None
if 'next_movement' not in st.session_state:
    st.session_state.next_movement = None

if 'data_excel' not in st.session_state:
    st.session_state.data_excel = []

if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'bot_name' not in st.session_state:
    st.session_state.bot_name = None


# role_user = "user"
# role_bot = "bot"


def on_chat_change():
    chat_box.use_chat_name(st.session_state["chat_name"])
    chat_box.context_to_session() # restore widget values to st.session_state when chat name changed



def process_story_data():
    now_idx_dialogue = st.session_state.now_idx_dialogue
    story_data = st.session_state.story_data
    data_excel = st.session_state.data_excel
    if story_data is not None:
        total_dialogues = len(story_data.dialogue_data)

        # 手动控制循环从 now_idx_dialogue + 1 开始
        idx = now_idx_dialogue + 1
        while idx < total_dialogues:
            row = story_data.dialogue_data[idx]

            # 如果有下一个对话，准备好下一个状态
            if idx + 1 < total_dialogues:
                next_row = story_data.dialogue_data[idx + 1]
                st.session_state.next_dialogue = next_row["bot_response"]
                st.session_state.next_movement = next_row["char_action"]
            bot_speak = row["bot_response"]
            char_action = row["char_action"]
            # 输出当前的对话
            if(st.session_state.user_name):
                bot_speak = bot_speak.replace('{{user}}',st.session_state.user_name)
                char_action = char_action.replace('{{user}}',st.session_state.user_name)    
            
            chat_box.ai_say([
                Markdown("(对话)" + bot_speak , in_expander=False, expanded=True, title="answer"),
            ])
            
            chat_box.ai_say(
                Markdown("(场景)" + char_action, in_expander=False, expanded=True, title="answer"),
            )
            # 更新局部变量和 session_state
            st.session_state.now_dialogue.append(row["bot_response"])
            st.session_state.now_movement.append(row["char_action"])
            st.session_state.now_sound_emotion.append(row["sound_emotion"])
            st.session_state.now_movement_sound.append(row["action_sound"])
            data_excel.append({
                "scene_definition": row["scene_definition"],
                "sequence_number": row["sequence_number"],
                "user_hardware_input": row["user_hardware_input"],
                "user_input": row["user_input"],
                "bot_response": row["bot_response"],
                "hardware_output": row["hardware_output"],
                "sound_emotion": row["sound_emotion"],
                "breathing_sound": row["breathing_sound"],
                "action_sound": row["action_sound"],
                "char_action": row["char_action"]
            })
            st.session_state.now_idx_dialogue = idx
            st.session_state.story_data = story_data
            st.session_state.data_excel = data_excel
            # 模拟延迟
            time.sleep(3)

            # 增加索引
            idx += 1


        
  

with st.sidebar:
    st.subheader('sex ai rebot llm')
    # chat_name = st.selectbox("Chat Session:", ["default", "chat1"], key="chat_name", on_change=on_chat_change)
    # chat_box.use_chat_name(chat_name)
    # streaming = st.checkbox('streaming', key="streaming")
    # in_expander = st.checkbox('show messages in expander', key="in_expander")
    # show_history = st.checkbox('show session state', key="show_history")
    chat_box.context_from_session(exclude=["chat_name"]) # save widget values to chat context

    st.divider()

    btns = st.container()

    file = st.file_uploader(
        "story excel",
        type=["xlsx", "xls"],
    )
    if(file):
        if(st.session_state.story_data is None):         
            st.session_state.story_data = StoryData(file)
    
    if user_name := st.chat_input('你想要给自己起的名字'):
        st.session_state.user_name = user_name
    if bot_name := st.chat_input('你想要给机器人起的名字'):
        st.session_state.bot_name = bot_name

    if st.button("清除 session"):
        st.session_state.clear()
        # st.experimental_rerun()
        
    def save_state():
        data_excel = st.session_state.data_excel
        
        if data_excel is not None:
            df = pd.DataFrame(data_excel)
            # st.write(data_excel)
            output = "dialogue_data.xlsx"
            df.to_excel(output, index=False)
            
            with open(output, "rb") as file:
                st.download_button("Download dialogue data", data=file, file_name="dialogue_data.xlsx", key="download")
        else:
            st.warning("No story data available to save.")

    # 添加保存状态的按钮
    if st.button("Save State"):
        save_state()
    
    

def on_feedback(
    feedback,
    chat_history_id: str = "",
    history_index: int = -1,
):
    reason = feedback["text"]
    score_int = chat_box.set_feedback(feedback=feedback, history_index=history_index) # convert emoji to integer
    # do something
    st.session_state["need_rerun"] = True


feedback_kwargs = {
    "feedback_type": "thumbs",
    "optional_text_label": "wellcome to feedback",
}

story_prompt = None



    
def get_ai_answer(prompt):
    print(prompt)
    if st.session_state.user_name:
        prompt = prompt.replace('{{user}}',st.session_state.user_name)
    if st.session_state.bot_name:
        prompt = prompt.replace('{{bot}}',st.session_state.bot_name)   

    # # ———————————————算法服务———————————————————
    from openai import OpenAI
    client = OpenAI(api_key="0",base_url="http://direct.virtaicloud.com:42275/v1")
    print("prompt ------------------------------------------------\n", prompt)
    messages = [{"role": "user", "content": prompt}]
    result = client.chat.completions.create(messages=messages,  model="/gemini/code/LLaMA-Factory_new/saves/CommandR-35B-Chat/full/train_2024-09-21-08-15-11/checkpoint-30/")
    print("response********************************************"+result.choices[0].message.content)
    assert len(result.choices[0].message.content)!=0
    st.write(result.choices[0].message.content)
    text = result.choices[0].message.content
    action_match = re.search(r'<动作描述.*?>(.*?)</动作描述>', text, re.DOTALL)
    dialogue_match = re.search(r'<对话内容.*?>(.*?)</对话内容>', text, re.DOTALL)
    action = action_match.group(1) if action_match else ""
    dialogue = dialogue_match.group(1) if dialogue_match else ""
    print(action, action)
    # # ——————————————————————————————————
    
    #mock
    # action  = "ls"
    # dialogue = "cds"
    return action ,dialogue

def continue_dialogue(query):
    # time.sleep(2)
    story_data = st.session_state.story_data
    # st.write("++++++++")
    # st.write( story_data.__dict__)
    now_dialogue = st.session_state.now_dialogue
    now_movement = st.session_state.now_movement
    now_sound_emotion = st.session_state.now_sound_emotion
    now_movement_sound = st.session_state.now_movement_sound
    next_dialogue = st.session_state.next_dialogue
    next_movement = st.session_state.next_movement
    role_user = "{{user}}"
    role_bot = "{{bot}}"
    if st.session_state.user_name:
        role_user = st.session_state.user_name
    if st.session_state.bot_name:
        role_bot = st.session_state.bot_name
    
    
    
    story_data.get_basic_story_prompt()
    story_data.get_dialogue_story(role=role_bot, dialogue=now_dialogue, movement=now_movement, sound_emotion=now_sound_emotion, movement_sound=now_movement_sound)
    story_data.get_next_dialogue(next_dialogue)
    st.session_state.story_data = story_data
    
    story_data.get_user_prompt(role_user,query)
    story_data.get_basic_story_prompt()
    prompt = story_data.get_fianl_story_prompt()
    action,dialogue = get_ai_answer(prompt)
    action.replace('{{user}}',role_user)
    action.replace('{{bot}}',role_bot)
    dialogue.replace('{{user}}',role_user)
    dialogue.replace('{{bot}}',role_bot)
    
    chat_box.ai_say([
        Markdown("（场景描述）" + action, in_expander=False, expanded=True, title="answer"),
    ])
    chat_box.ai_say([
        Markdown("（对话）" + dialogue, in_expander=False, expanded=True, title="answer"),
    ])
    data_excel = st.session_state.data_excel
    data_excel.append({
        "scene_definition": "",
        "sequence_number": "",
        "user_hardware_input": "",
        "user_input": query,
        "bot_response": dialogue,
        "hardware_output": "",
        "sound_emotion": "",
        "breathing_sound": "",
        "action_sound": "",
        "char_action": action
    })
    
    # st.info(data_excel)
    story_data.dialogue_story += f"""
    <对话内容 发起者={role_user}>
        <![CDATA[
        {query}
        ]]>
    </对话内容>
    
    """
    
    story_data.dialogue_story += f"""
        <动作描述 发起者={role_bot}>
            <![CDATA[
                {action}
            ]]>
        </动作描述>
        <对话内容 发起者={role_bot}>
            <![CDATA[
                {dialogue}
            ]]>
        </对话内容>
    """
    st.session_state.story_data = story_data
    
    
def replace_char_user(text, role_user, role_bot):
    text.replace(r'{{bot}}',  role_bot).replace(r'{{user}}', role_user) 
    return text

def user_input():
    if query := st.chat_input('input your question here'):
        # st.write(query)
        chat_box.user_say(query)
        st.session_state.session = True
        # now_idx_dialogue = st.session_state.now_idx_dialogue
        # 
        continue_dialogue(query)
        st.session_state.session = False

# story_data = StoryData()
# st.write("process story data")
# st.write("process story data done")
# st.write("user input")
user_input()
# st.write("user input done")
if st.button("Start Chat") :
    process_story_data()
