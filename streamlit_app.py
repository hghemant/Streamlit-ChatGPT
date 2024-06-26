import streamlit as st
import requests

# Define your page functions
def upload_document_page():
    st.title("Upload Document")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # Assuming you have set up your API as previously described
        files = {'file': uploaded_file.getvalue()}
        response = requests.post('https://your-api-gateway-url', files=files)
        if response.status_code == 200:
            st.success("File uploaded successfully!")
        else:
            st.error("Failed to upload file.")

def get_api_response(user_input, conversation_history, model_choice, top_k):
    api_url = 'https://your-api-url'  # Replace with your actual API URL
    payload = {
        "input": user_input,
        "conversation_history": conversation_history,
        "model": model_choice,
        "top_k": top_k
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        decoded_response = response.json()
        api_response = decoded_response.get('body', 'no response body')
        return api_response
    except Exception as e:
        print(f"Error processing the response: {e}")
        return f"An error occurred: {str(e)}"

def chatbot_page():
    st.sidebar.title("Chatbot Settings")
    model_choice = st.sidebar.selectbox(
        "LLM Model:",
        ["Cohere", "Claude 3.0 (Haiku)", "Claude 3.0 (Sonnet)"],
        index=0  # Default to the first option
    )

    top_k = st.sidebar.select_slider(
        "No. of chunks to be retrieved (top_k):",
        options=[5, 8, 10],
        value=5  # Default value
    )

    st.title("Chat Interface with History")

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    user_input = st.text_input("Type your message here...", key="user_input")

    if st.button("Send") and user_input:
        response = get_api_response(user_input, st.session_state.conversation_history, model_choice, top_k)
        st.session_state.conversation_history.insert(0, {"user": user_input, "bot": response})  # Insert at the start
        st.experimental_rerun()

    st.write("Conversation History:")
    for index, exchange in enumerate(st.session_state.conversation_history):
        st.text_area(label=f"You: {index+1}", value=exchange['user'], height=75, disabled=True, key=f"user_{index}")
        st.text_area(label=f"AI: {index+1}", value=exchange['bot'], height=150, disabled=True, key=f"bot_{index}")

# Sidebar for navigation
st.sidebar.title("Main Navigation")
choice = st.sidebar.radio("Go to", ("Upload Document", "Chatbot"))

# Display the selected page
if choice == "Upload Document":
    upload_document_page()
elif choice == "Chatbot":
    chatbot_page()
