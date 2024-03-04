import streamlit as st
import os
import time
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import google.generativeai as genai
from openai import OpenAI
from pypdf import PdfReader

# Retrieve the API keys from the environment variables
CLAUDE_API_KEY = os.environ["ANTHROPIC_API_KEY"]
GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]
CLIENT_API_KEY = os.environ['OPENAI_API_KEY']

anthropic = Anthropic(api_key=CLAUDE_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
client = OpenAI(api_key=CLIENT_API_KEY)

st.write("LHC's Garage :sunglasses: Testing Anthropic, Google and OpenAI's LLMs :sunglasses:")

Model_Option = st.selectbox("**Select** model:", ('claude-3-sonnet-20240229','claude-3-opus-20240229','claude-2.1','gemini-pro','gpt-3.5-turbo-0125','gpt-4-turbo-preview'))

Menu_Option = st.selectbox("**Select** analysis:", ('Summarise the key points of the text', 'Identify possible biases in the text', 'Seek views disagreeing with the text', 'Find angles missing from the text', 'Discuss broader significance of the topics', 'Compare the text with historical events', 'Customise your own unique prompt'))
if Menu_Option == "Summarise the key points of the text":
  instruction = "Summarise the key points of the text."
elif Menu_Option == "Identify possible biases in the text":
  instruction = "Identify possible biases in the text."
elif Menu_Option == "Seek views disagreeing with the text":
  instruction = "Offer perspectives that disagree with the text."
elif Menu_Option == "Find angles missing from the text":
  instruction = "Offer perspectives that are missing from the text."
elif Menu_Option == "Discuss broader significance of the topics":
  instruction = "Draft a conclusion that highlights the broader significance of the topics."
elif Menu_Option == "Compare the text with historical events":
  instruction = "Reflect on the text and draw similiarities and differences to historical events in the last century."
elif Menu_Option == "Customise your own unique prompt":
  instruction = st.text_input("Customise your own unique prompt:", "What are the follow up actions?")

uploaded_file = st.file_uploader("**Upload** the PDF document to analyse:", type = "pdf")
raw_text = ""
output_text = ""
if uploaded_file is not None:
  doc_reader = PdfReader(uploaded_file)
  for i, page in enumerate(doc_reader.pages):
    text = page.extract_text()
    if text:
      raw_text = raw_text + text + "\n"

  start = time.time()
  input = "Read the text below." + instruction + "\n\n" + raw_text


  if Model_Option == "claude-3-sonnet-20240229" or "claude-3-opus-20240229":  
    message = client.messages.create(
      model = Model_Option,
      max_tokens = 1000,
      temperature=0,
      system= "Be precise and concise.",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": input
            }
          ]
        }
      ]
    )
    output_text = message.content
  
  elif Model_Option == "claude-2.1":  
    completion = anthropic.completions.create(
      model=Model_Option,
      temperature = 0,
      max_tokens_to_sample=1000,
      prompt=f"{HUMAN_PROMPT} {input} {AI_PROMPT}",
    )
    output_text = completion.completion
  
  elif Model_Option == "gemini-pro":
    gemini = genai.GenerativeModel(Model_Option)
    response = gemini.generate_content(input)
    output_text = response.text
    st.write(response.prompt_feedback)  

  elif Model_Option == "gpt-3.5-turbo-0125" or Model_Option == "gpt-4-turbo-preview":
    response = client.chat.completions.create(
      model=Model_Option, messages=[
        {"role": "system", "content": ""},
        {"role": "user", "content": input},
      ],
      temperature=0,
    )
    output_text = response.choices[0].message.content
    
  end = time.time()
  
  st.write(output_text)
  st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
  st.download_button(':scroll:', output_text)
