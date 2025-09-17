import streamlit as st
import pandas as pd

# Function to find related URLs along with database names
def find_related_urls(data, topic):
    # Normalize the input topic and data for case insensitive matching
    data['database_name'] = data['database_name'].str.lower()
    topic = topic.lower()

    # Filter the rows where the database_name contains the topic
    filtered_data = data[data['database_name'].str.contains(topic, na=False)]
    # if the filtered data is empty, try to find the closest match in database_information
    if filtered_data.empty:
        filtered_data = data[data['database_information'].str.contains(topic, na=False)]

    if filtered_data.empty:
        return None
    # Return the database names and URLs from the filtered data
    return filtered_data[['database_name', 'database_url']]

# Load the data once (to avoid reloading on every interaction)
@st.cache_data
def load_data():
    csv_path = 'Clemson_Library_A_to_Z_database.csv'  # Update this path
    return pd.read_csv(csv_path)

data = load_data()

# Streamlit user interface
st.title('Clemson University Library Database Finder')
user_input = st.text_input("Enter a topic to search:", "")

if user_input:
    # Search for related database names and URLs
    related_data = find_related_urls(data, user_input)
    
    if related_data is not None:
        st.write("Related Databases and URLs:")
        for _, row in related_data.iterrows():
            st.markdown(f"**{row['database_name']}**")
            st.markdown(f"- {row['database_url']}")
    else:
        st.write("No related databases found for the given topic.")