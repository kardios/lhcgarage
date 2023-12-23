import streamlit as st
import os
import time
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from PyPDF2 import PdfReader

# Retrieve the OpenAI API key from the environment variables
API_KEY = os.environ["ANTHROPIC_API_KEY"]

anthropic = Anthropic(
    api_key = API_KEY,
)

st.write("LHC's Garage")
#instruction = st.text_input("Enter your prompt:", "How does a man become a god?")

Menu_Option = st.selectbox("Select analysis:", ('Shorten the text into a summary', 'Identify possible biases in the text', 'Seek views disagreeing with the text', 'Find angles missing from the text', 'Discuss broader significance of the topics', 'Compare the text with historical events', 'Customise your own unique prompt'))
if Menu_Option == "Shorten the text into a summary":
  instruction = "Generate a concise and coherent summary that includes the main ideas and key details."
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

uploaded_file = st.file_uploader("**Upload** the PDF document you would like me to analyse", type = "pdf")
raw_text = ""
output_text = ""
if uploaded_file is not None:
    doc_reader = PdfReader(uploaded_file)
    for i, page in enumerate(doc_reader.pages):
        text = page.extract_text()
        if text:
            raw_text = raw_text + text + "\n"

if st.button('Let\'s Go!'):
    start = time.time()
    input = "Read the text below." + instruction + "\n\n" + raw_text
    completion = anthropic.completions.create(
        model="claude-2.1",
        temperature = 0,
        max_tokens_to_sample=1000,
        prompt=f"{HUMAN_PROMPT} {input} {AI_PROMPT}",
    )
    output = completion.completion
    end = time.time()
    st.write(output)
    st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
