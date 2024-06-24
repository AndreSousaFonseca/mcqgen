import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging


#loading response json file:
with open("C:\Users\andre\mcqgen\Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

# Create a title for the form
st.title("MCQs Creator Aplication with Langchain")

# Create a form using st.form
with st.form("user_inputs"):
    #File upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file")  # Based on this file we will generate the MCQ

    #Input Fields
    mcq_count= st.number_input("No. of MCQs", min_value =3, max_value=50)

    #Subject
    subject= st.text_input("Insert Subject", max_chars=20)

    # Quiz Tone
    tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")

    # Add Button
    button= st.for_submit_buton("Create MCQs")

    # Check if the buttins is clicked and lall fileds have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=red_file(upload_file)
                #Count tokens an the cost of API call
                with get_openai_callback() as cb:
                    response=generator_evaluate_chain(
                        {
                            "text" : TEXT,
                            "number": NUMBER,
                            "subject": SUBJECT,
                            "tone": TONE,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens:{cb.total_Tokens}")
                print(f"Prompt Tokens:{cb.prompt_Tokens}")
                print(f"Completion Tokens:{cb.completion_Tokens}")
                print(f"Total Tokens:{cb.total_cost}")
                if isinstance(response,dict):
                    #Extract the quizz data from the response
                    quiz=response.get("quiz", None)
                    if quiz is not None:
                        table_data=get_table_Data(quiz)
                        if table_data is not None:
                            df=pd.DataFrmae(table_data)
                            df.inde+=df.index+1
                            st.table(df)
                            #Display the review in a text box as well
                            st.text_area(lalbe="Review", value=response("Review"))
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)


                
                

