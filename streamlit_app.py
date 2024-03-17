import streamlit as st
import requests

def get_api_response(user_input):
    api_url = "https://gqq75mttf2.execute-api.us-east-1.amazonaws.com/Test"
    payload = {"input": user_input}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        # Ensure that your API returns a JSON with a 'response' key
        api_response = response.json().get('response', 'No response from API.')
        return api_response
    except Exception as e:
        return f"An error occurred: {str(e)}"

def chat_interface():
    st.title("Chat Interface with History")

    # Initialize or update session state for holding conversation history
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    user_input = st.text_input("Type your message here...", key="user_input")
    
    if st.button("Send"):
        if user_input:
            # Fetch response from the API
            response = get_api_response(user_input)
            
            # Update conversation history in session state
            st.session_state.conversation_history.append({"user": user_input, "bot": response})
            
            # Clear the user input after sending the message
            st.session_state.user_input = ""
            
            # Display conversation history
            for exchange in st.session_state.conversation_history:
                st.text_area("You", value=exchange['user'], height=75, disabled=True)
                st.text_area("AI", value=exchange['bot'], height=150, disabled=True)

if __name__ == "__main__":
    chat_interface()
