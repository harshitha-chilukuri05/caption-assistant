import requests
import streamlit as st
from PIL import Image

st.set_page_config(page_title="📸 AI Instagram Caption Assistant")

# Get API key from Streamlit secrets
api_key = st.secrets["OPENROUTER_API_KEY"]

st.title("📸 AI Instagram Caption Assistant")

option = st.radio("Choose input type:", ["Upload a photo", "Enter a post description"])

user_input = ""
if option == "Upload a photo":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Photo", use_column_width=True)
        user_input = st.text_area("Briefly describe the image", placeholder="e.g., sunset at the beach")
else:
    user_input = st.text_area("Post description", placeholder="e.g., Coffee and calm mornings ☕🌞")

if st.button("✨ Generate Captions"):
    if not user_input:
        st.warning("Please provide a description.")
    else:
        with st.spinner("Generating..."):

            # Build request to OpenRouter
            headers = {
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://yourusername.streamlit.app",  # Replace with your Streamlit URL
                "Content-Type": "application/json"
            }

            body = {
                "model": "openai/gpt-3.5-turbo",  # or "mistralai/mistral-7b-instruct"
                "messages": [
                    {"role": "system", "content": "You create Instagram captions and hashtags."},
                    {"role": "user", "content": f"Write 3 creative Instagram captions and 5 trending hashtags for: {user_input}"}
                ]
            }

            try:
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
                data = response.json()
                result = data['choices'][0]['message']['content']
                st.success("✅ Captions and hashtags ready:")
                st.markdown(result)
            except Exception as e:
                st.error("❌ Error generating captions.")
                st.text(str(e))
