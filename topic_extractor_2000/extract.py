from langchain.chains import create_tagging_chain, create_tagging_chain_pydantic
from langchain_openai import ChatOpenAI
import pandas as pd
import json
import streamlit as st

def extract_topics(documents: list, topic_schema: str):
    """
    Extract topics from a list of documents using a given topic schema and model.
    """
    #topic_schema = json.loads(topic_schema)
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    chain = create_tagging_chain(topic_schema, llm)
    results = []
    for i, doc in enumerate(documents):
        results.append(chain.run(doc))
        results[-1] = {k.replace('?',''): v for k, v in results[-1].items()}
        st.sidebar.write(f'document {i} out of {len(documents)} processed')
    topics_df = pd.DataFrame(results)
    return topics_df

def create_schema(user_inputs: list) -> dict:
    """
    Create a topic schema from user inputs.
    """
    properties = {input: {"type": "string", "description": f"Nævner teksten {input}?", "enum": ["ja", "nej"]} for input in user_inputs}
    schema = {"properties": properties}
    return schema