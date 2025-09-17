import streamlit as st
import requests
import spacy

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

st.title('Clemson University Library Article Finder Chatbot')

# Initialize session state for chat history if it doesn't already exist
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = ""

def handle_general_statements(doc):
    greeting_words = ['hello', 'hi ', 'hey', 'hello!', 'hi!', 'hey!', 'greetings', 'good morning', 'good afternoon', 'good evening']
    thank_words = ['thanks', 'thank you', 'thx', 'appreciate', 'grateful', 'thank you!']
    help_words = ['help', 'assist', 'support', 'information', 'guide', 'how to', 'what is', 'what are']

    lower_doc = doc.text.lower()
    if any(word in lower_doc for word in greeting_words):
        return "Hello! How can I assist you today?"
    elif any(word in lower_doc for word in thank_words):
        return "You're welcome! Do you have any other questions?"
    elif any(word in lower_doc for word in help_words):
        return "What do you need help with? You can ask me about available articles or specific topics."
    return None

def analyze_query(query):
    doc = nlp(query)
    general_response = handle_general_statements(doc)
    if general_response:
        return general_response
    if any(token.pos_ == "NOUN" for token in doc):
        return None  # Continue with specific query processing
    return "Could you please specify what you are looking for or ask about another topic?"

def send_query_to_gemini(query):
    response = analyze_query(query)
    if response:
        return response  # Early return for general responses or errors
    gemini_endpoint = 'http://localhost:5000/gemini'
    try:
        response = requests.post(gemini_endpoint, json={'query': query})
        if response.status_code == 200:
            data = response.json()
            if data:
                # Format each entry as a Markdown hyperlink
                return "\n\n".join([f"{item['database_name']}:\n[{item['database_url']}]({item['database_url']})" for item in data])
            else:
                return "No related databases found for the given topic."
        return f"No related databases found for the given topic. Could you provide more details or ask about something else?"
    except requests.exceptions.RequestException as e:
        return f"Failed to reach the server: {e}"

def update_chat_log(user_input, response):
    # Prepend the new log entry at the top of the existing chat log
    new_log_entry = f"You: {user_input}\n\nChatbot:\n{response}\n\n"
    new_log_entry += "-" * 50 + "\n\n"
    st.session_state.chat_log = new_log_entry + st.session_state.chat_log

with st.form(key='query_form'):
    user_input = st.text_input("Type your query here:")
    submit_button = st.form_submit_button('Send')

if submit_button and user_input:
    response = send_query_to_gemini(user_input)
    update_chat_log(user_input, response)

# Use Markdown to display the chat log so links are clickable
st.markdown(st.session_state.chat_log, unsafe_allow_html=True)