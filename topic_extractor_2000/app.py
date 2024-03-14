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
st.write("input data")
st.write(df)

### Sidebar ###
st.sidebar.header("input")
user_topic_schema = st.sidebar.text_area('What topics do you want to extract?', value=default_schema, height=500)

### End sidebar ###

# Button to print a greeting in the main area when clicked
if st.sidebar.button('Extract topics'):
    # compute the topics
    st.sidebar.write(f'extracting topics...')
    json_topic_schema = json.loads(user_topic_schema)
    properties = list(json_topic_schema['properties'].keys())
    df_with_topics = extract_topics(df['review'].values, user_topic_schema)
    # Display result dataframe
    st.header("output data")
    df = df.join(df_with_topics)
    st.write(df)
    # Display the counts of the topics
    st.header('Topic counts')
    #counts = df[properties].count()
    counts = {column: df[column].value_counts() for column in properties}
    counts_df = pd.DataFrame(counts).fillna(0).astype(int).T
    #st.bar_chart(counts)

    # Plotting with Matplotlib
    fig, ax = plt.subplots()
    counts_df.plot(kind='bar', ax=ax)
    # Customize the plot if necessary (e.g., add labels, title)
    ax.set_xlabel('Categories')
    ax.set_ylabel('Counts')
    ax.set_title('Counts of "ja" and "nej"')
    # Show the plot in Streamlit
    st.pyplot(fig)
