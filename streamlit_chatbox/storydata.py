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
        dialogue_start_idx = excel_data[excel_data['剧本相关'] == '对话数据'].index[0] + 2

        # 提取对话数据
        self.dialogue_data = []
        for idx, row in excel_data.iloc[dialogue_start_idx:].iterrows():
            if  pd.isna(row['Unnamed: 4']):
                dialogue = row['Unnamed: 4']  # 对话内容
                self.dialogue_data.append({ "dialogue": dialogue})

# Streamlit界面
st.title("Excel 文件处理为 StoryData 对象")

# 文件上传
uploaded_file = st.file_uploader("上传一个Excel文件", type=["xlsx", "xls"])

if uploaded_file is not None:
    # 按钮用于处理文件并生成 StoryData 对象
    if st.button("处理并生成 StoryData"):
        # 通过文件初始化StoryData对象
        story_data = StoryData(uploaded_file)
        
        # 展示StoryData对象内容
        st.write("### 角色设定")
        st.text(story_data.character_info)
        
        st.write("### 任务设定")
        st.text(story_data.task_info)
        
        st.write("### 故事背景")
        st.text(story_data.story_background)
        
        st.write("### 对话数据")
        st.write(story_data.dialogue_data)
