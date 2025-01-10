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

class VirtualAgent:
    def __init__(self, name, personality, knowledge_base, initial_emotional_state):
        self.name = name
        self.personality = personality
        self.knowledge_base = knowledge_base
        self.emotional_state = initial_emotional_state

    def respond(self, message, context):
        prompt = self.create_prompt(message, context)
        response = model.generate_content(prompt)
        sentiment = self.analyze_sentiment(response.text.strip())
        return {
            "agent": self.name,
            "response": response.text.strip(),
            "sentiment": sentiment
        }

    def create_prompt(self, message, context):
        return f"You are a {self.personality} agent. Your expertise includes {', '.join(self.knowledge_base)}.\n" \
               f"Current emotional state: {self.emotional_state}.\n" \
               f"Context: {context}\n" \
               f"Message: {message}\n"

    def analyze_sentiment(self, text):
        positive_keywords = ["improve", "enhance", "good", "positive"]
        negative_keywords = ["risk", "problem", "concern", "negative"]
        if any(word in text for word in positive_keywords):
            return "positive"
        elif any(word in text for word in negative_keywords):
            return "negative"
        else:
            return "neutral"

# Example usage
agents = [
    VirtualAgent("LogicalClient", "rational", ["Contract Law", "Corporate Law"], "neutral"),
    VirtualAgent("EmotionalClient", "emotional", ["Family Law"], "anxious")
]

context = "Client wants to understand legal options for a family dispute."
message = "What are my chances in court?"

for agent in agents:
    response = agent.respond(message, context)
    print(f"{response['agent']} ({agent.personality}): {response['response']} (Sentiment: {response['sentiment']})")