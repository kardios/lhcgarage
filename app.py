import streamlit as st
import os
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

# Retrieve the OpenAI API key from the environment variables
API_KEY = os.environ["ANTHROPIC_API_KEY"]

anthropic = Anthropic(
    api_key = API_KEY,
)

st.write("LHC's Garage")
input = st.text_input("Enter your prompt:", "How does a man become a god?")

if st.button('Let\'s Go!'):
    completion = anthropic.completions.create(
        model="claude-2.1",
        temperature = 0,
        max_tokens_to_sample=1000,
        prompt=f"{HUMAN_PROMPT} {input} {AI_PROMPT}",
    )
output = completion.completion

st.write(output)
