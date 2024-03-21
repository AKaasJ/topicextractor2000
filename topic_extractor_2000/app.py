import streamlit as st
import pandas as pd
from extract import extract_topics, create_schema
import matplotlib.pyplot as plt

# Set the page layout
st.set_page_config(layout='wide')

# Title of the app
st.title('Topic Extractor 2000')

# Load the data
df = pd.read_csv('trustpilot.csv')
df.index = df.index + 1
st.header("Trustpilot reviews before classification:")
st.write(df)

### Sidebar ###
st.sidebar.header("Add topics you want to classify the reviews by:")

# Initialize session state for keeping track of text boxes
if 'num_textboxes' not in st.session_state:
    st.session_state['num_textboxes'] = 1

# Function to add a text box
def add_text_box():
    st.session_state['num_textboxes'] += 1

def reset_topics():
    st.session_state['num_textboxes'] = 1

# Button to add a new text box
col1, col2 = st.sidebar.columns(2)
with col1:
    st.button("Add topic to classify", on_click=add_text_box)
with col2:
    st.button("Reset topics", on_click=reset_topics)

sample_topics = {
    1: "Hunde- og dyreforsikringer",
    2: "Bådforsikringer",
    3: "Bilforsikringer",
    4: "Rejseforsikringer",
    5: "Indboforsikringer",
    6: "Ulykkesforsikringer",
    7: "Utilfredshed",
    8: "Priser",
}

# Display text boxes and store inputs in a list
user_inputs = []
for i in range(st.session_state['num_textboxes']):
    user_input = st.sidebar.text_input(f"Topic you want classified {i+1}", key=f"input_{i}", value = sample_topics.get(i+1, "placeholder emne"))
    user_inputs.append(user_input)

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
    st.write(df.fillna('N/A'))

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
