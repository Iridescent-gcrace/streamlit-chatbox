import streamlit as st
from streamlit_chatbox import *
import time
import simplejson as json

from streamlit_chatbox.storydata import StoryData
import threading

chat_box = ChatBox()
story_data = None
chat_box.use_chat_name("chat1") # add a chat conversatoin

def on_chat_change():
    chat_box.use_chat_name(st.session_state["chat_name"])
    chat_box.context_to_session() # restore widget values to st.session_state when chat name changed


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
    
    if st.button("Start Chat") and file:
        story_data = StoryData(file)
        
    

chat_box.init_session()
chat_box.output_messages()





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


def process_story_data():
    # dialogue_placeholder = st.empty()  # 占位符，用于动态更新对话内容
    now_dialogue = []
    now_movement = []
    now_sound_emotion = []
    now_movement_sound = []
    next_dialogue = None
    next_movement = None
    
    if story_data is not None:
        for idx, row in enumerate(story_data.dialogue_data):
            if session:
                if(idx + 1 < len(story_data.dialogue_data)):
                    next_row = story_data.dialogue_data[idx + 1]
                    next_dialogue = next_row["bot_response"]
                    next_movement = next_row["char_action"]
                
                break
            chat_box.ai_say([
                Markdown(row["bot_response"], in_expander=False, expanded=True, title="answer"),
            ])
            now_dialogue.append(row["bot_response"])
            now_movement.append(row["char_action"])
            now_sound_emotion.append(row["sound_emotion"])
            now_movement_sound.append(row["action_sound"])
            
            time.sleep(3)
    
    
def user_input():
    global session
    if query := st.chat_input('input your question here'):
        chat_box.user_say(query)
        session = True

session = False

process_story_data()

user_input()
