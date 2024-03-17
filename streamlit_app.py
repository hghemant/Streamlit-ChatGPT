import streamlit as st
import requests

# Function to get a response from an external API
def get_api_response(user_input, conversation_history):
    api_url = "https://gqq75mttf2.execute-api.us-east-1.amazonaws.com/Test"
    headers = {"Content-Type": "application/json"}
    payload = {
        "input": user_input,
        "conversation_history": conversation_history
    }
    
    try:
        # Here, include the conversation history in your API request if needed
        response = requests.post(api_url, json=payload, headers=headers)
        return response.json().get('response', 'No response from API')
    except Exception as e:
        return f"An error occurred: {str(e)}"

def chat_interface():
    st.title("Chat Interface with History")

    # Initialize conversation history if not present
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    # User input
    user_input = st.text_input("Type your message here...", key="user_input")

    # Handle the send action
    if st.button("Send") and user_input:
        # Fetch response from API, including the conversation history as context if needed
        response = get_api_response(user_input, st.session_state.conversation_history)
        
        # Update the conversation history
        st.session_state.conversation_history.append({"user": user_input, "bot": response})

        # Display each part of the conversation
        for exchange in st.session_state.conversation_history:
            st.text_area("You", value=exchange['user'], height=75, disabled=True)
            st.text_area("AI", value=exchange['bot'], height=150, disabled=True)
        
        # This workaround forces Streamlit to clear the input box after submission
        st.experimental_rerun()

if __name__ == "__main__":
    chat_interface()
