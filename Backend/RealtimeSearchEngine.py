from googlesearch import search
from groq import Groq
from json import load, dump
import datetime 
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

username = env_vars.get("username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

# write your information here
System = f"""Hello, I am {username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***"""

try:
    with open(r"Data\ChatLog.json", "r") as f:
        message = load(f)
except:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

def GoogleSearch(query):
    results = list(search(query, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"
    
    for i, result in enumerate(results, 1):
        Answer += f"{i}. {result}\n"  

    Answer += "[end]"
    return Answer

def AnswerModifier(answer):
    return "\n".join([line for line in answer.split("\n") if line.strip()])

SystemChatBot = [
    {"role": "system", "content": System},  # Fixed "System" -> "system"
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "How can I help you?"}
]

def Information():
    current_date_time = datetime.datetime.now()
    return f"""please use this real-time information if needed:
Day: {current_date_time.strftime("%A")}
Date: {current_date_time.strftime("%d")}
Month: {current_date_time.strftime("%B")}
Year: {current_date_time.strftime("%Y")}
Time: {current_date_time.strftime("%H")} hour {current_date_time.strftime("%M")} minutes {current_date_time.strftime("%S")} seconds
"""

def RealTimeSearchEngine(prompt):
    global SystemChatBot, message
    
    with open(r"Data\ChatLog.json", "r") as f:
        message = load(f)
    
    message.append({"role": "user", "content": prompt})  # Fixed f'{"prompt"}' -> prompt
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})  # Fixed "System" -> "system"
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + message,  # Fixed "System" -> "system"
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
    
    Answer = Answer.strip().replace("</s>", "")
    message.append({"role": "assistant", "content": Answer})
    
    with open(r"Data\ChatLog.json", "w") as f:
        dump(message, f, indent=4)
    
    SystemChatBot.pop()
    return AnswerModifier(Answer)

if __name__ == "__main__":
    while True:
        prompt = input("Enter your query >>> ")
        print(RealTimeSearchEngine(prompt))