import google.generativeai as genai
import os
from sklearn.metrics import accuracy_score, cohen_kappa_score
from collections import Counter

API_KEY = 'API_KEY'
with open('env.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    API_KEY = content

# 設定 Google Gemini API 金鑰
genai.configure(api_key=API_KEY)

# 初始化 Gemini 模型
model = genai.GenerativeModel('gemini-1.5-flash')

class LLM_Agent:
    def __init__(self, name, personality, strategy, knowledge):
        self.name = name
        self.personality = personality
        self.strategy = strategy
        self.knowledge = knowledge

    def respond(self, message, context):
        prompt = self.create_prompt(message, context)
        response = model.generate_content(prompt)
        sentiment = self.analyze_sentiment(response.text.strip())
        return {
            "agent": self.name,
            "personality": self.personality,
            "response": response.text.strip(),
            "sentiment": sentiment
        }

    def create_prompt(self, message, context):
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

    def analyze_sentiment(self, text):
        """
        簡單的情感分析：假設根據回應內容中是否包含正面或負面詞彙來判斷情感
        """
        positive_keywords = ["提升", "優化", "改善", "進步", "鼓勵"]
        negative_keywords = ["風險", "問題", "挑戰", "不足", "缺陷"]
        
        if any(word in text for word in positive_keywords):
            return "positive"
        elif any(word in text for word in negative_keywords):
            return "negative"
        else:
            return "neutral"

class LLM_MultiAgents:
    def __init__(self):
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
        self.sentiments = []  # 用於存儲所有回應的情感標籤

    def simulate_discussion(self, que, rounds=2):
        context = ""
        for round_num in range(1, rounds + 1):
            print(f"--- 第 {round_num} 輪討論 ---\n")
            for agent in self.agents:
                result = agent.respond(que, context)
                response, sentiment = result["response"], result["sentiment"]
                print(f"{result['agent']} ({result['personality']}): {response}")
                context += f"{response}\n"
                self.sentiments.append(sentiment)
            print("-" * 50)

    def evaluate_results(self):
        """
        評估情感分析的指標，包括準確率、一致性和 Kappa 值
        """
        # 假設真實情感標籤為 'positive'，模擬中可以根據具體場景調整
        true_sentiments = ["positive"] * len(self.sentiments)
        
        # 計算準確率
        accuracy = accuracy_score(true_sentiments, self.sentiments)
        
        # 計算情感一致性
        sentiment_counts = Counter(self.sentiments)
        most_common_sentiment = sentiment_counts.most_common(1)[0][0]
        consistency = sentiment_counts[most_common_sentiment] / len(self.sentiments)
        
        # 計算 Cohen’s Kappa
        kappa = cohen_kappa_score(true_sentiments, self.sentiments)
        
        print("\n--- 評估結果 ---")
        print(f"情感準確率 (Accuracy): {accuracy:.2f}")
        print(f"情感一致性 (Consistency): {consistency:.2f}")
        print(f"Cohen's Kappa: {kappa:.2f}")

# 測試 Multi-Agent 系統
if __name__ == "__main__":
    question1 = "如何提升聯邦學習的隱私保護和模型效能？"
    multi_agents = LLM_MultiAgents()
    multi_agents.simulate_discussion(question1, rounds=3)
    multi_agents.evaluate_results()