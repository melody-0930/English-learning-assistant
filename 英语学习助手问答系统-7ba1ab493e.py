import re
import json
import random
from collections import defaultdict

class EnglishLearningAssistant:
    def __init__(self):
        # 加载知识库和检索索引
        with open("english_course_knowledge.json", "r", encoding="utf-8") as f:
            self.knowledge_base = json.load(f)
        
        with open("english_course_search_index.json", "r", encoding="utf-8") as f:
            self.search_index = json.load(f)
        
        # 简单的停用词表
        self.stop_words = {"the", "a", "an", "and", "or", "but", "is", "are", "in", "on", "at", "to", "of", "for"}

    def extract_keywords(self, question):
        """提取问题中的关键词"""
        question_lower = question.lower()
        words = re.findall(r'\b\w+\b', question_lower)
        keywords = [word for word in words if word not in self.stop_words and len(word) > 2]
        return keywords

    def search_knowledge(self, keywords):
        """基于关键词搜索知识库"""
        results = defaultdict(list)
        
        for keyword in keywords:
            if keyword in self.search_index:
                for item in self.search_index[keyword]:
                    item_type = item["type"]
                    results[item_type].append(item)
        
        return results

    def generate_answer(self, question):
        """生成回答"""
        keywords = self.extract_keywords(question)
        if not keywords:
            return "抱歉，我没理解您的问题。请换一种方式提问。"
        
        results = self.search_knowledge(keywords)
        
        # 优先使用问答库中的标准答案
        if "qa" in results and results["qa"]:
            return results["qa"][0]["answer"]
        
        # 其次使用词汇解释
        if "vocabulary" in results and results["vocabulary"]:
            vocab_info = results["vocabulary"][0]
            return f"{vocab_info['word']} 的意思是：{vocab_info['definition']}"
        
        # 最后使用课文段落内容
        if "paragraph" in results and results["paragraph"]:
            # 取前两个相关段落
            paragraphs = [p["content"] for p in results["paragraph"][:2]]
            return "\n\n".join(paragraphs)
        
        # 如果没有找到匹配结果
        return "抱歉，我没有找到相关内容。您可以尝试询问与Unit 1课文相关的问题，例如：\n- What is the main idea of the president's speech?\n- What does 'triumph' mean?\n- Why does the president mention an alarm clock?"

    def run_demo(self):
        """运行问答演示"""
        print("===== 英语学习助手 =====")
        print("您可以提问关于Unit 1 'Fresh Start'的问题，输入'q'退出")
        
        while True:
            user_input = input("您的问题: ")
            if user_input.lower() == 'q':
                break
            
            answer = self.generate_answer(user_input)
            print(f"回答: {answer}\n")

if __name__ == "__main__":
    assistant = EnglishLearningAssistant()
    # 运行演示模式
    assistant.run_demo()
    # 保存问答系统实例（实际部署时使用）
    print("问答系统初始化完成，可以开始使用了！")