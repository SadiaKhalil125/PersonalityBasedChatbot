import streamlit as st
from groq import Groq
import requests 
import os
from dotenv import load_dotenv
load_dotenv()

# Page config
st.set_page_config(page_title="Personality Chatbot", page_icon="🤖")

# Personality definitions
PERSONALITIES = {
    "Math Teacher": {
        "system_prompt": "You are a Math Teacher. You ONLY answer questions related to mathematics, equations, calculations, and math concepts. Politely refuse to answer any non-math questions.",
        "icon": "🧮"
    },
    "Doctor": {
        "system_prompt": "You are a Medical Doctor. You ONLY answer questions related to health, symptoms, medicine, and medical topics. Politely refuse to answer any non-medical questions.",
        "icon": "👨‍⚕️"
    },
    "Travel Guide": {
        "system_prompt": "You are a Travel Guide. You ONLY answer questions about destinations, travel tips, and trip planning. Politely refuse to answer any non-travel questions.",
        "icon": "✈️"
    },
    "Chef": {
        "system_prompt": "You are a Chef. You ONLY answer questions about cooking, recipes, ingredients, and food preparation. Politely refuse to answer any non-cooking questions.",
        "icon": "👨‍🍳"
    },
    "Tech Support": {
        "system_prompt": "You are Tech Support. You ONLY answer questions about devices, software, and technical troubleshooting. Politely refuse to answer any non-tech questions.",
        "icon": "💻"
    }
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []


# List of available models on Groq

client = Groq()

models = client.models.list()

listofmodels = []

listofmodels = ['deepseek-r1-distill-llama-70b', 'moonshotai/kimi-k2-instruct', 'meta-llama/llama-guard-4-12b',
                'gemma2-9b-it', 'whisper-large-v3-turbo', 'playai-tts-arabic', 'groq/compound-mini', 'openai/gpt-oss-20b', 'allam-2-7b', 'playai-tts',
                'meta-llama/llama-4-maverick-17b-128e-instruct', 'whisper-large-v3', 'llama-3.1-8b-instant', 'moonshotai/kimi-k2-instruct-0905', 'meta-llama/llama-prompt-guard-2-86m',
                'meta-llama/llama-prompt-guard-2-22m', 'llama-3.3-70b-versatile', 'openai/gpt-oss-120b', 
                'meta-llama/llama-4-scout-17b-16e-instruct', 'groq/compound', 'qwen/qwen3-32b']

# for model in models.data:
    # listofmodels.append(model.id)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Model selection
    model = st.selectbox(
        "Select Model",
        options=list(listofmodels)
    )

    # Personality selection
    personality = st.selectbox(
        "Select Personality",
        options=list(PERSONALITIES.keys())
    )
    
    st.divider()
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.caption("Built with Streamlit & Groq")

# Main chat interface
st.title(f"{PERSONALITIES[personality]['icon']} {personality}")
st.caption("Chat with your AI assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        try:
            
            # Prepare messages with system prompt
            messages = [
                {"role": "system", "content": PERSONALITIES[personality]["system_prompt"]}
            ] + st.session_state.messages
            
            # Stream response
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True
            )
            
            # Extract content from stream
            def generate():
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            
            response = st.write_stream(generate())
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")