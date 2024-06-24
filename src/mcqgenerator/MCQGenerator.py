import os
import json
import traceback
import pandas as pd
from dotenv  import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
from langchain.callbacks import get_openai_callback

# Importing necessary packages from langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain


# Load environment variables from the .env file
load_dotenv()

# Access the envrionment variables just like we would with os.envrion
key=os.getenv("OPENAI_API_KEY")

# Create my OpenAI model 
llm = ChatOpenAI(open_ai_key=key, model_name="gpt-3.5-turbo", temperature = 0.3)


# Crete my imput prompt template
template = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is yout job to \
create a quiz of {number} multiple coice questions for {subject} students in {tone} tone.
make sure the questions are nor repeate and check all teh questions to ve conforming the text as well.
MAke sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensrude to make {number} MCQs
### REPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=['text', 'number', 'subject', 'tone', 'number', 'response_json'],
    template = template)

# Create a chain object
quiz_chain = LLMChain(llm = llm, prompt = quiz_generation_prompt, output_key="quiz", verbose = True)

template2 = """
You are an expert grammarian and write. Give me a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 word for complexity. 
If the quiz is not at per with cognitive and analytical abilities of the students.\.
Update the quiz questions which needs to be changed and change the tone that it perfectly fits the students  abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(input_variables = [ "subject", "quiz"], template = template2)

review_chain = LLMChain(llm = llm, prompt = quiz_evaluation_prompt, output_key="review", verbose = True)

generate_evaluate_chain = SequentialChain(
    chains= [quiz_chain, review_chain], 
    input_variables=['text', 'number', 'subject', 'tone', 'number', 'response_json'],
    output_variables=["quiz", "review"], 
    verbose= True
)

