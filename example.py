import streamlit as st
from streamlit_chatbox import *
import time
import simplejson as json

from streamlit_chatbox.storydata import StoryData
import threading


llm = FakeLLM()
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
    if st.button("Load Json") and file:
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

def process_story_data():
    # dialogue_placeholder = st.empty()  # 占位符，用于动态更新对话内容

    if story_data is not None:
        for idx, row in enumerate(story_data.dialogue_data):
            if session:
                break
            chat_box.ai_say([
                Markdown(row["bot_response"], in_expander=False, expanded=True, title="answer"),
            ])
            time.sleep(3)

def user_input():
    global session
    if query := st.chat_input('input your question here'):
        chat_box.user_say(query)
        session = True

session = False

process_story_data()

user_input()
    # if streaming:
    #     generator = llm.chat_stream(query)
    #     elements = chat_box.ai_say(
    #         [
    #             # you can use string for Markdown output if no other parameters provided
    #             Markdown("thinking", in_expander=in_expander,
    #                      expanded=True, title="answer"),
    #             Markdown("", in_expander=in_expander, title="references"),
    #         ]
    #     )
    #     time.sleep(1)
    #     text = ""
    #     for x, docs in generator:
    #         text += x
    #         chat_box.update_msg(text, element_index=0, streaming=True)
    #     # update the element without focus
    #     chat_box.update_msg(text, element_index=0, streaming=False, state="complete")
    #     chat_box.update_msg("\n\n".join(docs), element_index=1, streaming=False, state="complete")
    #     chat_history_id = "some id"
    #     chat_box.show_feedback(**feedback_kwargs,
    #                             key=chat_history_id,
    #                             on_submit=on_feedback,
    #                             kwargs={"chat_history_id": chat_history_id, "history_index": len(chat_box.history) - 1})
    # else:
    #     text = llm.chat(query)
    #     chat_box.ai_say(
    #         [
    #             Markdown(text, in_expander=in_expander,
    #                      expanded=True, title="answer"),
    #             # Markdown("\n\n".join(docs), in_expander=in_expander,
    #             #          title="references"),
    #         ]
    #     )

# cols = st.columns(2)
# if cols[0].button('show me the multimedia'):
#     chat_box.ai_say(Image(
#         'https://tse4-mm.cn.bing.net/th/id/OIP-C.cy76ifbr2oQPMEs2H82D-QHaEv?w=284&h=181&c=7&r=0&o=5&dpr=1.5&pid=1.7'))
#     time.sleep(0.5)
#     chat_box.ai_say(
#         Video('https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'))
#     time.sleep(0.5)
#     chat_box.ai_say(
#         Audio('https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'))

# if cols[1].button('run agent'):
#     chat_box.user_say('run agent')
#     agent = FakeAgent()
#     text = ""

#     # streaming:
#     chat_box.ai_say() # generate a blank placeholder to render messages
#     for d in agent.run_stream():
#         if d["type"] == "complete":
#             chat_box.update_msg(expanded=False, state="complete")
#             chat_box.insert_msg(d["llm_output"])
#             break

#         if d["status"] == 1:
#             chat_box.update_msg(expanded=False, state="complete")
#             text = ""
#             chat_box.insert_msg(Markdown(text, title=d["text"], in_expander=True, expanded=True))
#         elif d["status"] == 2:
#             text += d["llm_output"]
#             chat_box.update_msg(text, streaming=True)
#         else:
#             chat_box.update_msg(text, streaming=False)

# btns.download_button(
#     "Export Markdown",
#     "".join(chat_box.export2md()),
#     file_name=f"chat_history.md",
#     mime="text/markdown",
# )

# btns.download_button(
#     "Export Json",
#     chat_box.to_json(),
#     file_name="chat_history.json",
#     mime="text/json",
# )







# if show_history:
#     st.write(st.session_state)
