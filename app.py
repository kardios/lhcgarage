import streamlit as st
import os
import time
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from openai import OpenAI
from pypdf import PdfReader

# Retrieve the API keys from the environment variables
CLIENT_API_KEY = os.environ['OPENAI_API_KEY']
CLAUDE_API_KEY = os.environ["ANTHROPIC_API_KEY"]
GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]

client = OpenAI(api_key=CLIENT_API_KEY)
anthropic = Anthropic(api_key=CLAUDE_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

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

st.write("LHC's Garage :sunglasses: Test Cutting Edge LLMs")

Model_Option = st.selectbox("**Select** model:", ('GPT-4 Turbo','Claude 3 Opus','Gemini 1.5 Pro'))

Option_Action = st.selectbox("What should I do with your input?", ('Shorten into a summary', 'Condense into key points', 'Identify possible biases', 'Identify disagreeing views', 'Identify missing angles', 'Create alternative mental models', 'Discuss broader significance', 'Compare with historical events', 'Black swans and grey rhinos', 'Generate markdown summary', 'Customise your own prompt'))
if Option_Action == "Shorten into a summary":
  instruction = "You are my reading assistant. You will read the input I provide. Generate a concise and coherent summary. Identify the main ideas and key details. Present your output in a clear and organised way, as one single paragraph only."
elif Option_Action == "Condense into key points":
  instruction = "You are my reading assistant. You will read the input I provide. Summarize the input into bullet points. Identify the main ideas and key details, and condense them into concise bullet points. Recognize the overall structure of the text and create bullet points that reflect this structure. The output should be presented in a clear and organized way. Do not start with any titles."
elif Option_Action == "Identify possible biases":
  instruction = "You are my reading assistant. You will read the input I provide. Highlight any possible biases in the input in a clear and organised way, as one or more paragraphs."
elif Option_Action == "Identify disagreeing views":
  instruction = "You are my reading assistant. You will read the input I provide. Offer perspectives that disagree with the input in a clear and organised way, as one or more paragraphs."
elif Option_Action == "Identify missing angles":
  instruction = "You are my reading assistant. You will read the input I provide. Offer perspectives that are missing from the input in a clear and organised way, as one or more paragraphs."
elif Option_Action == "Create alternative mental models":
  instruction = "You are my reading assistant. You will read the input I provide. Generate three alternative mental models to consider the topics in the input in a clear and organised way."
elif Option_Action == "Discuss broader significance":
  instruction = "You are my reading assistant. You will read the input I provide. Draft a conclusion that highlights the broader significance of the topics in the input. Present the output in a clear and organised way, as one or more paragraphs."
elif Option_Action == "Compare with historical events":
  instruction = "You are my reading assistant. You will read the input I provide. Reflect on the input and draw similiarities and differences to historical events in the last century. Present the output in a clear and organised way, as one or more paragraphs."
elif Option_Action == "Black swans and grey rhinos":
  instruction = "You are my reading assistant. You will read the input I provide. Generate black swan and grey rhino scenarios from the input. The scenarios should sound plausible and coherent, draw inspiration from actual historical events, and highlight the impact. As I am familiar with the definition of black swans and grey rhinos, there is no need to explain what they are and you can jump straight into the list of scenarios. Present your output in bullet points under the headings Black Swans and Grey Rhinos."
elif Option_Action == "Generate markdown summary":
  instruction = "You are my reading assistant. You will read the input I provide. Use the input to generate a mindmap in Markdown format. Present your output as follows:\n\n# (Root)\n\n## (Branch 1)\n - (Branchlet 1a)\n - (Branchlet 1b)\n\n## (Branch 2)\n - (Branchlet 2a)\n - (Branchlet 2b)\n\n(and so on...)"
elif Option_Action == "Customise your own prompt":
  instruction = "You are my reading assistant. You will read the input I provide." + st.text_input("Customise your own unique prompt:", "What are the follow up actions?")

uploaded_file = st.file_uploader("**Upload** the PDF document to analyse:", type = "pdf")
raw_text = ""
output_text = ""
if uploaded_file is not None:
  doc_reader = PdfReader(uploaded_file)
  for i, page in enumerate(doc_reader.pages):
    text = page.extract_text()
    if text:
      raw_text = raw_text + text + "\n"

  with st.spinner("Running AI Model..."):
    
    start = time.time()
    
    input = "Read the text below." + instruction + "\n\n" + raw_text
    
    if Model_Option == "Claude 3 Opus":  
      message = anthropic.messages.create(
        model = "claude-3-opus-20240229",
        max_tokens = 1000,
        temperature = 0,
        system= "",
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
      output_text = message.content[0].text
  
    elif Model_Option == "Gemini 1.5 Pro":
      gemini = genai.GenerativeModel("gemini-1.5-pro-latest")
      response = gemini.generate_content(input)
      st.write(response.prompt_feedback)
      output_text = response.text

    elif Model_Option == "GPT-4 Turbo":
      response = client.chat.completions.create(
        model="gpt-4-turbo-preview", messages=[
          {"role": "system", "content": ""},
          {"role": "user", "content": input},
        ],
        temperature=0,
      )
      output_text = response.choices[0].message.content
    
    end = time.time()
  
  st.write(output_text)
  st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
  #st.download_button(':scroll:', output_text)
