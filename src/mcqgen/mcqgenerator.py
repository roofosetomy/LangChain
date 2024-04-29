import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqgen.logger import logging
from src.mcqgen.utils import read_file, get_table_data


from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain


load_dotenv()
KEY  = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=KEY, model="gpt-3.5-turbo", temperature=0.5)

TEMPLATE = """
Text:{text}
You are an expert mcq maker. Given the above text, it is your job to creat {number} of 
questions for {subject} students in {tone}.ensure to make {number} of question without repeatition.
make sure to format your reponse like response_json blow.
### response_json
{response_json}
"""

quiz_gen_prompt = PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template=TEMPLATE
)

quiz_chain = LLMChain(llm=llm,prompt=quiz_gen_prompt,output_key="quiz", verbose=True)



TEMPLATE2 = """
you are an expert english grammarian and writer. given a mcq for {subject} student.
Evaluate the complexity and update the questions needs to change to match with the abilities of students.
mcq quiz:{quiz}.
check from an expert english writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(input_variables=["subject","quiz"],template=TEMPLATE2)

review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt,output_key="review",verbose=True)



gen_eval_chain = SequentialChain(chains=[quiz_chain,review_chain], input_variables=["text","number","subject","tone","response_json"],
                                  output_variables=["quiz","review"], verbose=True)