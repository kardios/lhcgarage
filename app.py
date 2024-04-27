import streamlit as st
import os
import time
import telebot
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from openai import OpenAI
from groq import Groq
from pypdf import PdfReader

# Set up Telegram Bot
recipient_user_id = os.environ['RECIPIENT_USER_ID']
bot_token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(bot_token)

# Retrieve the API keys from the environment variables
CLIENT_API_KEY = os.environ['OPENAI_API_KEY']
CLAUDE_API_KEY = os.environ["ANTHROPIC_API_KEY"]
GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]
MISTRAL_API_KEY = os.environ["GROQ_API_KEY"]

client = OpenAI(api_key=CLIENT_API_KEY)
anthropic = Anthropic(api_key=CLAUDE_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
mistral = Groq(api_key=MISTRAL_API_KEY)

safety_settings = {
  HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
  HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
  HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
  HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

generation_config = genai.GenerationConfig(
  candidate_count = 1,
  temperature = 0,
)

st.set_page_config(page_title="Dempsey Labz", page_icon=":sunglasses:",)

with open("documentation.txt") as doc_file:
    doc_text = doc_file.read()

groq_output = mistral.chat.completions.create(
  model="mixtral-8x7b-32768", messages=[
    {"role": "system", "content": "You are Dempsey Labz, an intern. Compose a catchy and impactful introduction in one concise and coherent paragraph."},
    {"role": "user", "content": doc_text},
  ],
  temperature = 0.9,
)
intro_container = st.container(border=True)
intro_container.write(groq_output.choices[0].message.content)

prompt_title_list = []
prompt_text_list = []
prompt_filename_list = os.listdir("prompts")
for prompt_filename in prompt_filename_list:
  with open("prompts/" + prompt_filename) as prompt_file:
    prompt_text = prompt_file.read()
  prompt_title = prompt_filename.rstrip(".txt")
  prompt_title = prompt_title.replace("_"," ")
  prompt_title_list.append(prompt_title)
  prompt_text_list.append(prompt_text)
prompt_title_list.append("Customise your own prompt")
prompt_text_list.append("You are an amazing intern. I would like you to read the sources I provide. Generate a timeline of events.")

Prompt_Option = st.selectbox("Which Prompt do I use?", prompt_title_list)
index = prompt_title_list.index(Prompt_Option)

Customised_Prompt = st.text_area("You may wish to modify the prompt below.", prompt_text_list[index])

#Model_Option = st.selectbox("What Large Language Model do I use?", ('GPT-4 Turbo','Claude 3 Opus','Gemini 1.5 Pro'))

input_text = ""
free_text = st.text_area("Enter your free text data source and click **Let\'s Go :rocket:**")
uploaded_files = st.file_uploader("Upload your PDF data sources and click **Let\'s Go :rocket:**", 
                                  type = "pdf", accept_multiple_files = True)

for uploaded_file in uploaded_files:
  raw_text = ""
  if uploaded_file is not None:
    raw_text = raw_text + "\n**[START OF A SOURCE]**\n"
    doc_reader = PdfReader(uploaded_file)
    for i, page in enumerate(doc_reader.pages):
      text = page.extract_text()
      if text:
        raw_text = raw_text + text + "\n"
    raw_text = raw_text + "\n**[END OF A SOURCE]**\n"
  input_text = input_text + raw_text

if st.button("Let\'s Go! :rocket:"):

  if free_text.strip() != "":
    input_text = "\n**[START OF A SOURCE]**\n" + free_text + "\n**[END OF A SOURCE]**\n" + input_text 
  
  with st.spinner("Running AI Model..."):
    start = time.time()
    prompt = Customised_Prompt + "\n\n" + input_text
    gemini = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = gemini.generate_content(prompt, safety_settings = safety_settings, generation_config = generation_config)
    answer = response.text
    end = time.time()

    container = st.container(border=True)
    container.write(answer.replace("\n","  \n"))
    container.write("Time to generate: " + str(round(end-start,2)) + " seconds")
    bot.send_message(chat_id=recipient_user_id, text="Dempsey Labz")
    st.download_button(':floppy_disk:', answer)
