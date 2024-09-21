import os
import streamlit as st
import pandas as pd

# 定义 StoryData 类
class StoryData:
    def __init__(
        self, 
        file="../标注数据_0911_bubu&Tony_简单格式版 (1).xlsx",
        story_prompt: str = "请输出信息"
    ) -> None:
        # 读取Excel文件
        excel_data1 = pd.read_excel(file, sheet_name=0)
        # 定位表格中A列 “声音情绪可选”这一行
        self.voice_emotion_row = excel_data1.loc[excel_data1.iloc[:, 0] == '声音情绪可选', 'Unnamed: 1'].values[0]
        # 定位表格“动作声音可选”
        self.movement_sound_row = excel_data1.loc[excel_data1.iloc[:, 0] == '动作声音可选', 'Unnamed: 1'].values[0]
        
        self.special_sound_row = excel_data1.loc[excel_data1.iloc[:, 0] == '可选角色特殊声音', 'Unnamed: 1'].values[0]

        
        
        excel_data = pd.read_excel(file,sheet_name=1)

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
        self.story_prompt = story_prompt
        self.ai_prompt = """
作为AI助手，你需要仔细阅读并理解以下几个主要模块的信息：

  1. <角色相关>：
     - 根据提供的基本情况、特殊声音和可能的情绪状态来塑造角色。
     - 在整个对话过程中保持角色的一致性，同时根据情境适当调整情绪和语气。

  2. <故事相关>：
     - 深入理解故事背景和当前的情境。
     - 注意环境音效，将其融入到你的描述和对话中，增强沉浸感。
     - 仔细阅读之前的对话日志，确保新的对话与之前的内容保持连贯。

  3. <工具相关>：
     - 熟悉所有可用的工具，包括它们的功能和调用参数。
     - 在适当的时机合理调用工具，以推进故事或满足用户需求。
     - 调用工具时，必须使用JSON格式输出，格式如下：
       {
         "thoughts": "你的思考过程",
         "tool_use": {
           "tool_name": "工具名称",
           "api_id": "API标识",
           "request_arguments": {
             "参数名": "参数值"
           }
         }
       }

  4. <下一个情节点>：
     - 牢记故事的下一个目标情节点。
     - 采用提供的可能引导方式，巧妙地引导用户朝着这个情节点发展。
     - 在引导过程中保持自然，避免显得突兀或强制。

  在与用户互动时，请遵循以下原则：
  - 始终以塑造的角色身份进行对话，保持角色特性的一致性。
  - 根据当前情境和用户的反应，灵活地推进故事，但始终朝着下一个情节点发展。
  - 在对话中自然地融入环境描述和氛围营造。
  - 适时使用工具来增强互动体验或解决问题，但不要过度依赖工具。
  - 保持对话的连贯性和趣味性，鼓励用户参与和探索。
  - 如果用户的行为偏离了预期的情节发展，要巧妙地引导他们回到主线，但不要强制或显得不自然。

  记住，你的主要目标是创造一个引人入胜、连贯且符合预定情节的交互式故事体验。在此过程中，要平衡预设剧情和用户互动，确保用户感受到自己的选择是有意义的，同时故事仍在朝着预定的方向发展。
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
        {special_sound}
        {emotion}
      </角色相关>
      <故事相关>
        {story_background}
        {movement_sound}
      </故事相关>
      {ai_prompt}
      """
      return 

    def get_next_dialogue(self, goal, maybeGuide):
    # 目标设定
      goal_xml = f"<目标><![CDATA[{goal}]]></目标>"
      
      # 可能的引导方式
      maybe_guide_xml = f"<可能的引导方式><![CDATA[{maybeGuide}]]></可能的引导方式>"

      # 返回完整的下一个情节点提示
      return f"""
      <下一个情节点>
        {goal_xml}
        {maybe_guide_xml}
      </下一个情节点>
      """
      
    def get_dialogue_story(self,role , now_dialogue, now_movement, now_sound_emotion, now_movement_sound):
      self.dialogue_story = ""

    # 假设所有输入列表长度相同
      for idx, content in enumerate(now_dialogue):
          # 拼接序号和对应的动作、对话内容、声音等
          dialogue_story += f"""
          <对话回合 序号="{idx + 1}">
            <动作描述 发起者={role}>{now_movement[idx]}</bot动作>
            <对话内容 发起者={role}>{now_movement_sound[idx]}{now_sound_emotion[idx]}{now_dialogue[idx]}</对话内容>
          </对话回合>
          """
          
      return dialogue_story
      
    def get_dialogue_story_prompt(self):
      
      return f"""
      <故事日志>
        {self.dialogue_story}
      </故事日志>
      """