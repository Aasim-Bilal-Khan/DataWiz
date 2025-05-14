import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-70b-8192"
)

template = """
You are a highly accurate SQL generator. Use the following schema and user question to generate SQL.

Schema:
{schema}

Question:
{question}

SQL Query:
"""

prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template=template
)

sql_chain = LLMChain(llm=llm, prompt=prompt)
