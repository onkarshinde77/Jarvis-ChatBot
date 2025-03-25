from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
from mtranslate import translate

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-US")  # Default to English

# Fix incorrect replacement
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';

            recognition.continuous = true;
            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
        }
    </script>
</body>
</html>'''

HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Save the HTML file
current_dir = os.getcwd()
os.makedirs("Data", exist_ok=True)  # Ensure directory exists
with open("Data/Voice.html", "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Set up WebDriver
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
# chrome_options.add_argument("--headless=new")                 # for open chrome tab

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Paths
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
os.makedirs(TempDirPath, exist_ok=True)  # Ensure directory exists

def setAssistantStatus(Status):
    with open(os.path.join(TempDirPath, "Status.data"), "w", encoding="utf-8") as file:
        file.write(Status)

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_word = ['how','what','who','where','when','why','which','whose','whom','can you',"what's",'wh']
    
    if any(word + " " in new_query for word in question_word):
        new_query = new_query.rstrip(".?!") + "?"
    else:
        new_query = new_query.rstrip(".?!") + "."

    return new_query.capitalize()

def UniversalTranslator(text):
    return translate(text, "en", "auto").capitalize()

def SpeechRecognition():
    driver.get(f'file:///{current_dir}/Data/Voice.html')
    driver.find_element(By.ID, "start").click()
    
    while True:
        try:
            TextElement = driver.find_element(By.ID, "output")
            Text = TextElement.text.strip()
            if Text:
                driver.find_element(By.ID, "end").click()
                return QueryModifier(Text if 'en' in InputLanguage.lower() else UniversalTranslator(Text))
        except:
            pass

if __name__ == "__main__":
    while True:
        print(SpeechRecognition())
