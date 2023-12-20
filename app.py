import streamlit as st
import os
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from PyPDF2 import PdfReader

# Retrieve the OpenAI API key from the environment variables
API_KEY = os.environ["ANTHROPIC_API_KEY"]

anthropic = Anthropic(
    api_key = API_KEY,
)

st.write("LHC's Garage")
instruction = st.text_input("Enter your prompt:", "How does a man become a god?")

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
    input = instruction + "\n\n" + raw_text
    completion = anthropic.completions.create(
        model="claude-2.1",
        temperature = 0,
        max_tokens_to_sample=1000,
        prompt=f"{HUMAN_PROMPT} {input} {AI_PROMPT}",
    )
    output = completion.completion
    st.write(output)
