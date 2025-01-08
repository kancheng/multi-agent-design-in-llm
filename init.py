# import google.generativeai as genai
# import os

# genai.configure(api_key='AIzaSyBAObNpUQI03OopMPIwhaXCuc86sbls5R8')

# model = genai.GenerativeModel('gemini-1.5-flash')
# response = model.generate_content("What is federated learning?")
# print(response.text)

import google.generativeai as genai
import os

API_KEY = ''
with open('env.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    API_KEY = content

# 設定 Google Gemini API 金鑰
genai.configure(api_key=API_KEY)

# 初始化 Gemini 模型
model = genai.GenerativeModel('gemini-1.5-flash')

class LLM_Agent:
    def __init__(self, name, personality, strategy, knowledge):
        """
        初始化每個 Agent 的屬性
        """
        self.name = name
        self.personality = personality
        self.strategy = strategy
        self.knowledge = knowledge

    def respond(self, message):
        """
        使用 Gemini 模型根據不同策略與知識生成回應
        """
        prompt = self.create_prompt(message)
        response = model.generate_content(prompt)
        return f"{self.name} ({self.personality}): {response.text.strip()}"

    def create_prompt(self, message):
        """
        根據策略與知識庫生成對應的提示 (prompt)
        """
        prompt_base = f"You are a {self.personality} agent. You have expertise in the following areas: {', '.join(self.knowledge)}.\n"
        prompt_question = f"Based on your knowledge, provide a response to: '{message}'\n"
        
        if self.strategy == "logic":
            return prompt_base + "Focus on providing a logical and data-driven solution.\n" + prompt_question
        elif self.strategy == "creative":
            return prompt_base + "Focus on providing an innovative and outside-the-box solution.\n" + prompt_question
        elif self.strategy == "cautious":
            return prompt_base + "Focus on identifying potential risks and concerns.\n" + prompt_question
        elif self.strategy == "optimistic":
            return prompt_base + "Focus on providing an encouraging and solution-oriented response.\n" + prompt_question
        else:
            return prompt_base + prompt_question

class LLM_MultiAgents:
    def __init__(self):
        """
        初始化多個 Agents，並賦予特定知識庫
        """
        self.agents = [
            LLM_Agent("LogicMaster", "理性", "logic", [
                "Differential Privacy", "Secure Multi-Party Computation", 
                "Federated Averaging Algorithm", "Distributed System Optimization"
            ]),
            LLM_Agent("CreativeThinker", "創意", "creative", [
                "Generative Adversarial Networks (GAN)", "Semi-Supervised Learning", 
                "Stochastic Augmentation Strategies", "Graph-Based Federated Learning"
            ]),
            LLM_Agent("CautiousAnalyst", "謹慎", "cautious", [
                "Risk Analysis in Federated Learning", "Convergence and Stability Factors", 
                "Resource Cost Analysis", "Common Attack Vectors"
            ]),
            LLM_Agent("OptimisticPlanner", "樂觀", "optimistic", [
                "Progressive Privacy Enhancement", "Federated Learning Applications", 
                "Rapid Deployment and Testing Strategies", "Efficient Collaborative Optimization"
            ]),
        ]

    def simulate_discussion(self, que):
        """
        模擬多個 Agents 的討論
        """
        print(f"問題: {que}\n")
        for agent in self.agents:
            response = agent.respond(que)
            print(response)
            print("-" * 50)

# 測試 Multi-Agent 系統
if __name__ == "__main__":
    question1 = "如何提升聯邦學習的隱私保護和模型效能？"
    question2 = "如何規劃日本旅遊行程？"
    question3 = "如何向喜歡的異性告白？"
    question4 = "台灣半導體與供應鏈的人工智能工程師如何有計畫的準備台灣的律師考試？"
    question5 = "如何準備德語考試？"
    question6 = "如何準備日語考試？"
    multi_agents = LLM_MultiAgents()
    multi_agents.simulate_discussion(question1)
    print("=" * 50)
    multi_agents.simulate_discussion(question2)
    print("=" * 50)
    multi_agents.simulate_discussion(question3)
    print("=" * 50)
    multi_agents.simulate_discussion(question4)
    print("=" * 50)
    multi_agents.simulate_discussion(question5)
    print("=" * 50)
    multi_agents.simulate_discussion(question6)
