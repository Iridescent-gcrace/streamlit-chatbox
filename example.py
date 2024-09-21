import streamlit as st
from streamlit_chatbox import *
import time
import simplejson as json


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


role_user = "user"
role_bot = "bot"


def on_chat_change():
    chat_box.use_chat_name(st.session_state["chat_name"])
    chat_box.context_to_session() # restore widget values to st.session_state when chat name changed



def process_story_data():
    # 检查st.session_state中是否已经有变量，如果没有则初始化


    # 从st.session_state中获取变量
    now_idx_dialogue = st.session_state.now_idx_dialogue

    story_data = st.session_state.story_data

    if story_data is not None:
        for idx, row in enumerate(story_data.dialogue_data[now_idx_dialogue+2:]):
            # st.write(st.session_state.session)
            if (idx + 1 < len(story_data.dialogue_data)):
                next_row = story_data.dialogue_data[idx + 1]
                st.session_state.next_dialogue = next_row["bot_response"]
                st.session_state.next_movement = next_row["char_action"]
            st.session_state.now_idx_dialogue = idx
                # break
            chat_box.ai_say([
                Markdown(row["bot_response"], in_expander=False, expanded=True, title="answer"),
            ])

            # 更新st.session_state中的变量
            st.session_state.now_dialogue.append(row["bot_response"])
            st.session_state.now_movement.append(row["char_action"])
            st.session_state.now_sound_emotion.append(row["sound_emotion"])
            st.session_state.now_movement_sound.append(row["action_sound"])

            time.sleep(3)

        
  

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
        st.session_state.story_data = StoryData(file)
    

        
    







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



    
def get_ai_answer(query):
    return "test ai answer"

def continue_dialogue(query):
    story_data = st.session_state.story_data
    # st.write("++++++++")
    # st.write( story_data.__dict__)
    now_idx_dialogue = st.session_state.now_idx_dialogue
    now_dialogue = st.session_state.now_dialogue
    now_movement = st.session_state.now_movement
    now_sound_emotion = st.session_state.now_sound_emotion
    now_movement_sound = st.session_state.now_movement_sound
    next_dialogue = st.session_state.next_dialogue
    next_movement = st.session_state.next_movement
    story_data.get_basic_story_prompt()
    story_data.get_dialogue_story(role="bot", dialogue=now_dialogue, movement=now_movement, sound_emotion=now_sound_emotion, movement_sound=now_movement_sound)
    story_data.get_next_dialogue(next_dialogue, next_movement)
    st.session_state.story_data = story_data
    
    story_data.get_user_prompt(role_user,query)
    story_data.get_basic_story_prompt()
    prompt = story_data.get_fianl_story_prompt()
    ai_answer = get_ai_answer(prompt)
    chat_box.ai_say([
        Markdown(ai_answer, in_expander=False, expanded=True, title="answer"),
    ])
    story_data.dialogue_story += f"""
    <对话内容 发起者={role_user}>
        <![CDATA[
        {query}
        ]]>
      </对话内容>
    
    """
    
    story_data.dialogue_story += f"""
        <对话内容 发起者={role_bot}>
        <![CDATA[
        {ai_answer}
        ]]>
    """
    st.session_state.story_data = story_data
    
def user_input():
    if query := st.chat_input('input your question here'):
        # st.write(query)
        chat_box.user_say(query)
        st.session_state.session = True
        continue_dialogue(query)
        st.session_state.session = False

if st.button("Start Chat") :
    process_story_data()
# story_data = StoryData()
# st.write("process story data")
# st.write("process story data done")
# st.write("user input")
user_input()
# st.write("user input done")
