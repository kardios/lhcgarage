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
st.write("**Dempsey Labz**, your AI intern")

with open("documentation.txt") as doc_file:
    doc_text = doc_file.read()

with st.expander("Click to read documentation"):
  st.write(doc_text)

prompt_filename_list = os.listdir("prompts")
for prompt_filename in prompt_filename_list:
  with open("prompts/" + prompt_filename) as prompt_file:
    prompt_text = prompt_file.read()
  groq_output = mistral.chat.completions.create(
    model="mixtral-8x7b-32768", messages=[
      {"role": "system", "content": ""},
      {"role": "user", "content": prompt_text},
    ],
    temperature = 0,
  )
  prompt_title = groq_output.choices[0].message.content
  st.write(prompt_title)

Model_Option = st.selectbox("What Large Language Model do I use?", ('GPT-4 Turbo','Claude 3 Opus','Gemini 1.5 Pro'))

Option_Input = st.selectbox("How will I receive your input?", ('Upload a pdf','Enter free text'))
