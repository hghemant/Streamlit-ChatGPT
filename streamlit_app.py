import streamlit as st
import requests


def get_api_response(user_input, conversation_history, model_choice, top_k):
    api_url = "https://gqq75mttf2.execute-api.us-east-1.amazonaws.com/Test"
    payload = {
        "input": user_input,
        "conversation_history": conversation_history,
        "model": model_choice,  # Including the selected model in the payload
        "top_k": top_k  # Including the number of chunks to be retrieved
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


def chat_interface():
    st.sidebar.title("Settings")
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
        st.session_state.conversation_history.append({"user": user_input, "bot": response})
        st.experimental_rerun()


    st.write("Conversation History:")
    for index, exchange in enumerate(st.session_state.conversation_history):
        st.text_area(label=f"You: {index+1}", value=exchange['user'], height=75, disabled=True, key=f"user_{index}")
        st.text_area(label=f"AI: {index+1}", value=exchange['bot'], height=150, disabled=True, key=f"bot_{index}")


if __name__ == "__main__":
    chat_interface()




