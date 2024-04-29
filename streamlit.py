import os
import json
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from src.mcqgen.utils import read_file, get_table_data
from src.mcqgen.mcqgenerator import gen_eval_chain
from src.mcqgen.logger import logging


with open (r'./response.json', 'r') as file:
    response_json = json.load(file)


st.title("MCQ generator with langchain")

with st.form("user inputs"):
    uploaded_file = st.file_uploader("upload a text file")
    mcq_count = st.number_input("No. of MCQ", min_value=3, max_value=50)
    subject = st.text_input("insert subject", max_chars=20)
    tone = st.text_input("complexity level", max_chars=20, placeholder="Simple")
    button = st.form_submit_button("create mcq")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file()
                with get_openai_callback() as cb:
                    try:
                        response = gen_eval_chain(
                            {
                                "text" : text,
                                "number" : mcq_count,
                                "subject" : subject,
                                "tone" : tone,
                                "response_json" : json.dumps(response_json)
                            }
                        )   
                    except:
                        st.text_area(label="review", value="Result fetched. API KEY required to display the output.")
            except:
                print("ERROR..")
            print(response)
