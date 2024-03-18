# Import the Streamlit library
import streamlit as st
#from sklearn.datasets import fetch_20newsgroups
import pandas as pd
from extract import extract_topics
import json
import matplotlib.pyplot as plt
#newsgroups_train = fetch_20newsgroups(data_home=".")

default_schema = """{
    "properties": {
        "Priser": {
            "type": "string",
            "description": "Er priser nævnt i teksten?",
            "enum": ["ja", "nej"]
        },
        "Båd": {
            "type": "string",
            "description": "Nævner teksten bådforsikringer?",
            "enum": ["ja", "nej"]
        },
        "hund eller dyr": {
            "type": "string",
            "description": "Nævner teksten hunde eller andre dyreforsikringer?",
            "enum": ["ja", "nej"]
        },
        "Skade": {
            "type": "string",
            "description": "Nævner teksten en skade eller forsikringssag?",
            "enum": ["ja", "nej"]
        }
    }
}"""

#def main():
st.set_page_config(layout='wide')
# Title of the app
st.title('Topic Extractor 2000')

#documents = newsgroups_train.data[0:5]
#df = pd.DataFrame({'Emails': documents})
df = pd.read_csv('trustpilot.csv')
df.index = df.index + 1
st.write("Trustpilot reviews before classification:")
st.write(df)

### Sidebar ###
st.sidebar.header("Add topics you want to extract from reviews")
#user_topic_schema = st.sidebar.text_area('What topics do you want to extract?', value=default_schema, height=500)

# Initialize session state for keeping track of text boxes
if 'num_textboxes' not in st.session_state:
    st.session_state['num_textboxes'] = 1

# Function to add a text box
def add_text_box():
    st.session_state['num_textboxes'] += 1

# Button to add a new text box
st.sidebar.button("Add topic to extract", on_click=add_text_box)

# Display text boxes and store inputs in a list
user_inputs = []
for i in range(st.session_state['num_textboxes']):
    user_input = st.sidebar.text_input(f"Topic you want extracted {i+1}", key=f"input_{i}", value = "dyreforsikringer")
    user_inputs.append(user_input)


def create_schema(user_inputs: list) -> dict:
    """
    Create a topic schema from user inputs.
    """
    properties = {input: {"type": "string", "description": f"Nævner teksten {input}?", "enum": ["ja", "nej"]} for input in user_inputs}
    schema = {"properties": properties}
    return schema

### End sidebar ###

# Button to print a greeting in the main area when clicked
if st.sidebar.button('Classify reviews'):
    # compute the topics
    st.sidebar.write(f'Classifying documents...')
    json_topic_schema = create_schema(user_inputs)

    properties = list(json_topic_schema['properties'].keys())
    df_with_topics = extract_topics(df['Review'].values, json_topic_schema)
    # Display result dataframe
    st.header("Trustpilot reviews after classification:")
    df = df.join(df_with_topics)
    st.write(df)
    # Display the counts of the topics
    st.header('Topic counts')
    counts = {column: df[column].value_counts() for column in df_with_topics.columns}
    
    counts_df = pd.DataFrame(counts).fillna(0).astype(int).T

    # Plotting with Matplotlib
    fig, ax = plt.subplots()
    counts_df.plot(kind='bar', ax=ax)
    # Customize the plot if necessary (e.g., add labels, title)
    ax.set_xlabel('Categories')
    ax.set_ylabel('Counts')
    ax.set_title('Counts of "ja" and "nej"')
    # Show the plot in Streamlit
    st.pyplot(fig)
