import streamlit as st
import requests
import json


def get_api_response(user_input, conversation_history):
    api_url = "https://gqq75mttf2.execute-api.us-east-1.amazonaws.com/Test"
    payload = {
        "input": user_input,
        "conversation_history": conversation_history
    }
    headers = {"Content-Type": "application/json"}


    try:
        response = requests.post(api_url, json=payload, headers=headers)
        # First, let's print the entire response to inspect its structure
        print("Full API Response:", response.text)


        # Attempt to decode the JSON response
        decoded_response = response.json()
        print("Decoded JSON Response:", decoded_response)


        # If the body is a stringified JSON, it needs to be loaded
        body_str = decoded_response.get('body', '{}')  # Assuming 'body' is a string
        print("Body String (Pre-Load):", body_str)


        # Now, let's try to parse the string in 'body' as JSON
        body = json.loads(body_str)
        print("Body Content (Post-Load):", body)


        # Extracting the 'completion' field from the loaded 'body'
        api_response = body.get('completion', 'No completion in response')
        return api_response
    except Exception as e:
        print(f"Error processing the response: {e}")
        return f"An error occurred: {str(e)}"








def chat_interface():
    st.title("Chat Interface with History")


    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []


    user_input = st.text_input("Type your message here...", key="user_input")


    if st.button("Send") and user_input:
        response = get_api_response(user_input, st.session_state.conversation_history)
        st.session_state.conversation_history.append({"user": user_input, "bot": response})
        st.experimental_rerun()


    for index, exchange in enumerate(st.session_state.conversation_history):
        st.text_area(label="You: ", value=exchange['user'], height=75, disabled=True, key=f"user_{index}")
        st.text_area(label="AI: ", value=exchange['bot'], height=150, disabled=True, key=f"bot_{index}")


if __name__ == "__main__":
    chat_interface()




