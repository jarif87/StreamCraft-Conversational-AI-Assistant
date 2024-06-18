import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables from .env file
load_dotenv()

# Configure the Google AI SDK with the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up the generative model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Set up Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Chat Bot", page_icon=":panda_face:")
st.title("StreamCraft Conversational AI Assistant")

# Function to get response from the Gemini model
def get_response(query, chat_history):
    # Prepare the chat history in the required format
    history = [{"parts": [{"text": msg['content']}], "role": "user" if msg['type'] == "human" else "model"} for msg in chat_history]
    chat_session = model.start_chat(history=history)
    try:
        response = chat_session.send_message(query)
        return response.text
    except genai.types.StopCandidateException as e:
        return e.candidate.text

# Conversation rendering
for message in st.session_state.chat_history:
    if message['type'] == "human":
        with st.chat_message("Human"):
            st.markdown(message['content'])
    else:
        with st.chat_message("AI"):
            st.markdown(message['content'])

# User input
user_query = st.chat_input("Your Message")

if user_query:
    st.session_state.chat_history.append({"type": "human", "content": user_query})

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = get_response(user_query, st.session_state.chat_history)
        st.markdown(ai_response)

    st.session_state.chat_history.append({"type": "ai", "content": ai_response})
