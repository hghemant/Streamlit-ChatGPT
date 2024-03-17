import streamlit as st
import requests

def get_api_response(user_input):
    api_url = "https://your.api.endpoint"
    payload = {
        "input": user_input
    }
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        api_response = response.json()['response']
        return api_response
    except Exception as e:
        return f"An error occurred: {str(e)}"


def chat_interface():
    st.title("Chat Interface")

    user_input = st.text_input("Type your message here...", key="user_input")

    
    if st.button("Send"):
        if user_input:
            response = get_api_response(user_input)
            st.text_area("Response", value=response, height=300, disabled=True)

if __name__ == "__main__":
    chat_interface()
