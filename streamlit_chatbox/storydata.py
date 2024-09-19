import os
import streamlit as st
import pandas as pd

# 定义 StoryData 类
class StoryData:
    def __init__(self, file):
        # 读取Excel文件
        excel_data = pd.read_excel(file)

        # 提取表格中的不同部分
        self.character_info = excel_data.loc[excel_data['剧本相关'] == '角色设定', 'Unnamed: 1'].values[0]
        self.task_info = excel_data.loc[excel_data['剧本相关'] == '任务设定', 'Unnamed: 1'].values[0]
        self.story_background = excel_data.loc[excel_data['剧本相关'] == '故事背景', 'Unnamed: 1'].values[0]

        # 找到“对话数据”的起始行
        dialogue_start_idx = excel_data[excel_data['剧本相关'] == '对话数据'].index[0] + 1

                # 提取从“对话数据”之后的内容
        self.dialogue_data = []
        print(excel_data.iloc[dialogue_start_idx:].iterrows())
        os.write(1, f"{excel_data.iloc[dialogue_start_idx:].iterrows()}\n".encode()) 

        # for idx, row in excel_data.iloc[dialogue_start_idx:].iterrows():
        #     st.write(f"行 {idx}: {row.to_dict()}")  # 将每行内容转换为字典格式并显示

            # 确保 bot 回复不为空
        self.dialogue_data = []
        for idx, row in excel_data.iloc[dialogue_start_idx:].iterrows():
            if not pd.isna(row['Unnamed: 5']):  # 确保'bot'（假设第6列）的列数据不为空
                dialogue_entry = {
                    "scene_definition": row['Unnamed: 3'],  # 场景定义 (假设为第1列)
                    "sequence_number": row['Unnamed: 1'],  # 序号 (假设为第2列)
                    "user_hardware_input": row['Unnamed: 2'],  # 用户硬件输入 (假设为第3列)
                    "user_input": row['Unnamed: 3'],  # 用户输入 (假设为第4列)
                    "bot_response": row['Unnamed: 4'],  # 机器人回复 (假设为第5列)
                    "hardware_output": row['Unnamed: 5'],  # 硬件输出（可选） (假设为第6列)
                    "sound_emotion": row['Unnamed: 7'],  # 声音情绪（必选） (假设为第7列)
                    "breathing_sound": row['Unnamed: 8'],  # 喘息声音（可选） (假设为第8列)
                    "action_sound": row['Unnamed: 9'],  # 动作声音（可选） (假设为第9列)
                    "char_action": row['Unnamed: 10']  # 角色动作（可选） (假设为第10列)
                }
                self.dialogue_data.append(dialogue_entry)
# Streamlit界面测试导出方式
# st.title("Excel 文件处理为 StoryData 对象")

# # 文件上传
# uploaded_file = st.file_uploader("上传一个Excel文件", type=["xlsx", "xls"])

# if uploaded_file is not None:
#     # 按钮用于处理文件并生成 StoryData 对象
#     if st.button("处理并生成 StoryData"):
#         # 通过文件初始化StoryData对象
#         story_data = StoryData(uploaded_file)
        
#         # 展示StoryData对象内容
#         st.write("### 角色设定")
#         st.text(story_data.character_info)
        
#         st.write("### 任务设定")
#         st.text(story_data.task_info)
        
#         st.write("### 故事背景")
#         st.text(story_data.story_background)
        
#         st.write("### 对话数据")
#         st.write(story_data.dialogue_data)
