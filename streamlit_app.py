import streamlit as st
import requests

def get_api_response(user_input, conversation_history):
    # Placeholder for your API URL
    api_url = "https://gqq75mttf2.execute-api.us-east-1.amazonaws.com/Test"
    payload = {
        "input": user_input,
        "conversation_history": conversation_history
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        # Make sure your API returns a response in the expected format
        api_response = response.json().get('response', 'No response from API')
        return api_response
    except Exception as e:
        return f"An error occurred: {str(e)}"

def chat_interface():
    st.title("Chat Interface with History")

    # Initialize conversation history if not present
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    user_input = st.text_input("Type your message here...", "")

    if st.button("Send") and user_input:
        # Fetch response from API
        response = get_api_response(user_input, st.session_state.conversation_history)
        
        # Update the conversation history
        st.session_state.conversation_history.append({"user": user_input, "bot": response})

        # Clear the input (workaround by rerunning the app)
        st.experimental_rerun()

    # Display conversation history
    for index, exchange in enumerate(st.session_state.conversation_history):
        st.text_area(label=f"You: ", value=exchange['user'], height=75, disabled=True, key=f"user_{index}")
        st.text_area(label="AI: ", value=exchange['bot'], height=150, disabled=True, key=f"bot_{index}")

if __name__ == "__main__":
    chat_interface()
