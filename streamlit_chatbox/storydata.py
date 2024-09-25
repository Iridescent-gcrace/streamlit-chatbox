import os
import streamlit as st
import pandas as pd
import re

# 定义 StoryData 类
class StoryData:
    def __init__(
        self, 
        file="../标注数据.xlsx",
        story_prompt: str = "请输出信息"
    ) -> None:
        # 读取Excel文件
        excel_data1 = pd.read_excel(file, sheet_name=0)
        self._excel1 = excel_data1
        # 定位表格中A列 “声音情绪可选”这一行
        self.voice_emotion_row = excel_data1.loc[excel_data1.iloc[:, 0] == '声音情绪可选', 'Unnamed: 1'].values[0]
        # 定位表格“动作声音可选”
        self.movement_sound_row = excel_data1.loc[excel_data1.iloc[:, 0] == '动作声音可选', 'Unnamed: 1'].values[0]
        
        self.special_sound_row = excel_data1.loc[excel_data1.iloc[:, 0] == '喘息声音可选', 'Unnamed: 1'].values[0]

        
        
        excel_data = pd.read_excel(file,sheet_name=1)
        self._excel2 = excel_data
        # 提取表格中的不同部分
        self.character_info = excel_data.loc[excel_data['剧本相关'] == '人物设定', 'Unnamed: 1'].values[0]
        self.task_info = excel_data.loc[excel_data['剧本相关'] == '任务设定\nconstrain\n无关话题处理方式\n建议行为', 'Unnamed: 1'].values[0].replace("{{char}}", '顾恒')
        self.story_background = excel_data.loc[excel_data['剧本相关'] == '此次故事背景', 'Unnamed: 1'].values[0]
        self.guidence = excel_data.loc[excel_data['剧本相关'] == '引导', 'Unnamed: 1'].values[0]
 
        # 找到“对话数据”的起始行
        dialogue_start_idx = excel_data[excel_data['剧本相关'] == '对话数据'].index[0] + 1
        # self.data_excel = []
        # 提取从“对话数据”之后的内容
        print(excel_data.iloc[dialogue_start_idx:].iterrows())
        # os.write(1, f"{excel_data.iloc[dialogue_start_idx:].iterrows()}\n".encode()) 

        # for idx, row in excel_data.iloc[dialogue_start_idx:].iterrows():
        #     st.write(f"行 {idx}: {row.to_dict()}")  # 将每行内容转换为字典格式并显示

            # 确保 bot 回复不为空
        self.dialogue_data = []
        for idx, row in excel_data.iloc[dialogue_start_idx:].iterrows():
            if not pd.isna(row['Unnamed: 5']):  # 确保'bot'（假设第6列）的列数据不为空
                dialogue_entry = {
                    "scene_definition": row[0],  # 场景定义 (假设为第1列)
                    "sequence_number": row[1],  # 序号 (假设为第2列)
                    "user_hardware_input": row[2],  # 用户硬件输入 (假设为第3列)
                    "user_input": row[3],  # 用户输入 (假设为第4列)
                    "bot_response": row[4],  # 机器人回复 (假设为第5列)
                    "hardware_output": row[5],  # 硬件输出（可选） (假设为第6列)
                    "sound_emotion": row[6],  # 声音情绪（必选） (假设为第7列)
                    "breathing_sound": row[7],  # 喘息声音（可选） (假设为第8列)
                    "action_sound": row[8],  # 动作声音（可选） (假设为第9列)
                    "char_action": row[9]  # 角色动作（可选） (假设为第10列)
                }
                print(dialogue_entry)
                self.dialogue_data.append(dialogue_entry)
        self.story_prompt = story_prompt
        self.ai_prompt = f"""
<指令>
  <![CDATA[
  作为{{bot}}，你需要仔细阅读并理解以下几个主要模块的信息：

  1. <角色相关>：
     - 根据提供的基本情况、特殊声音和可能的情绪状态来塑造顾恒。
     - 在整个对话过程中保持角色的一致性，同时根据情境适当调整情绪和语气。

  2. <故事相关>：
     - 深入理解故事背景和当前的情境。
     - 注意环境音效，将其融入到你的描述和对话中，增强沉浸感。
     - 仔细阅读之前的对话日志，确保新的对话与之前的内容保持连贯。

  4. <下一个情节点>：
     - 牢记故事的下一个目标情节点。
     - 采用提供的可能引导方式，巧妙地引导用户朝着这个情节点发展。
     - 在引导过程中保持自然，避免显得突兀或强制。

  在与用户互动时，请遵循以下原则：
  - {self.task_info}
  - 始终以塑造的角色身份进行对话，保持角色特性的一致性。
  - 根据当前情境和用户的反应，灵活地推进故事，但始终朝着下一个情节点发展。
  - 在对话中自然地融入环境描述和氛围营造。
  - 适时使用工具来增强互动体验或解决问题，但不要过度依赖工具。
  - 保持对话的连贯性和趣味性，鼓励用户参与和探索。
  - 如果用户的行为偏离了预期的情节发展，要巧妙地引导他们回到主线，但不要强制或显得不自然。
  - 这是一个模拟对话的场景，因此每次你需要回复一句话
  - 对话的输出格式是：
    <动作描述 发起者="{{bot}}"></动作描述>
    <对话内容 发起者="{{bot}}"></对话内容>

  ]]>
  </指令>
  
  """    
    def get_basic_story_prompt(self):
    # 故事角色相关设定
      character_info = f"<角色设定><![CDATA[{self.character_info}]]></角色设定>"
      special_sound = f"<可选特殊角色声音><![CDATA[{self.special_sound_row}]]></可选特殊角色声音>"
      emotion = f"<可选角色情绪><![CDATA[{self.voice_emotion_row}]]></可选角色情绪>"

      # 故事背景相关设定
      story_background = f"<故事背景><![CDATA[{self.story_background}]]></故事背景>"
      movement_sound = f"<可选故事环境音><![CDATA[{self.movement_sound_row}]]></可选故事环境音>"

      # AI的指令
      ai_prompt = f"<指令><![CDATA[{self.ai_prompt}]]></指令>"

      # 返回完整的故事提示
      self.basic_prompt =  f"""
      <角色相关>
        {character_info}
        {emotion}
        {special_sound}
      </角色相关>
      <故事相关>
        {story_background}
        {movement_sound}
      </故事相关>
      {ai_prompt}
      """
      return 

    def replace_you_and_me(self, text):
      text = re.sub(r'我', '{{char}}', text)
      text = re.sub(r'你', '{{user}}', text) 
      return text
    
    
    def get_next_dialogue(self, goal):
    # 目标设定
      #goal = self.replace_you_and_me(goal)
      goal = goal.replace("你", "{{user}}").replace("我", '顾恒')
      goal_xml = f"<目标><![CDATA[{goal}]]></目标>"
      
      # 可能的引导方式
      #maybe_guide_xml = self.replace_you_and_me(self.guidence)
      maybe_guide_xml = f"<可能的引导方式><![CDATA[{self.guidence}]]></可能的引导方式>"

      # 返回完整的下一个情节点提示
      self.next_dialogue =  f"""
      <下一个情节点>
        {goal_xml}
        {maybe_guide_xml}
      </下一个情节点>
      """
      return
      
    def get_dialogue_story(self, role, 
                           dialogue, movement, sound_emotion, movement_sound):
      self.dialogue_story = ""

    # 假设所有输入列表长度相同
      for idx, content in enumerate(dialogue):
          # 拼接序号和对应的动作、对话内容、声音等
          now_movement = movement[idx]
          now_sound_emotion = sound_emotion[idx]
          now_movement_sound = movement_sound[idx]
          now_dialogue = dialogue[idx]
          now_movement = now_movement.replace("你", "{{user}}").replace("我", '顾恒')
          #now_sound_emotion = self.replace_you_and_me(now_sound_emotion)
          #now_movement_sound = self.replace_you_and_me(now_movement_sound)
          self.dialogue_story += f"""
          <对话回合 序号="{idx + 1}">
            <动作描述 发起者={role}>![CDATA[{now_movement}][</bot动作>
            <对话内容 发起者={role}>![CDATA[{now_movement_sound}{now_sound_emotion}{now_dialogue}]</对话内容>
          </对话回合>
          """
          

    def get_user_prompt(self, role = 'user', input = ''):
      #input = self.replace_you_and_me(input)
      self.user_prompt = f"""
        <对话内容 发起者="{role}">
          <![CDATA[
            {input}
          ]]>
        </对话内容>
      
      """
    
    def get_fianl_story_prompt(self):
      return f"""
      <提示>
        {self.basic_prompt}
        {self.next_dialogue}
        <故事日志>
          {self.dialogue_story}
        <故事日志>
        {self.user_prompt}
      </提示>
      """