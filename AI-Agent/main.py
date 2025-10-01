import streamlit as st
from groq import Groq

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

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Model selection
    model = st.text_input("Model Name", value="llama-3.3-70b-versatile", help="Enter Groq model name")
    
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
            client = Groq()
            
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