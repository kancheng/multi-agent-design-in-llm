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

    def respond(self, message, context):
        """
        使用 Gemini 模型根據不同策略與知識生成回應，並根據上下文進行調整
        """
        prompt = self.create_prompt(message, context)
        response = model.generate_content(prompt)
        return f"{self.name} ({self.personality}): {response.text.strip()}"

    def create_prompt(self, message, context):
        """
        根據策略與知識庫生成對應的提示 (prompt)，並結合上下文進行多輪回應
        """
        prompt_base = f"You are a {self.personality} agent. You have expertise in the following areas: {', '.join(self.knowledge)}.\n"
        prompt_context = f"Here is the previous context of the discussion: '{context}'\n"
        prompt_question = f"Based on your knowledge, provide a response to: '{message}'\n"
        
        if self.strategy == "logic":
            return prompt_base + prompt_context + "Focus on providing a logical and data-driven solution.\n" + prompt_question
        elif self.strategy == "creative":
            return prompt_base + prompt_context + "Focus on providing an innovative and outside-the-box solution.\n" + prompt_question
        elif self.strategy == "cautious":
            return prompt_base + prompt_context + "Focus on identifying potential risks and concerns.\n" + prompt_question
        elif self.strategy == "optimistic":
            return prompt_base + prompt_context + "Focus on providing an encouraging and solution-oriented response.\n" + prompt_question
        else:
            return prompt_base + prompt_context + prompt_question

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

    def simulate_discussion(self, que, rounds=2):
        """
        模擬多個 Agents 的多輪討論，每輪基於上一輪的回應進行調整
        """
        print(f"問題: {que}\n")
        context = ""
        
        for round_num in range(1, rounds + 1):
            print(f"--- 第 {round_num} 輪討論 ---\n")
            for agent in self.agents:
                response = agent.respond(que, context)
                print(response)
                context += f"{response}\n"  # 更新上下文
            print("-" * 50)

# 測試 Multi-Agent 系統
if __name__ == "__main__":
    question1 = "如何提升聯邦學習的隱私保護和模型效能？"
    multi_agents = LLM_MultiAgents()
    multi_agents.simulate_discussion(question1, rounds=3)