# app.py

import openai
import streamlit as st
from PIL import Image

st.set_page_config(page_title="📸 AI Instagram Caption Assistant")

# Add your OpenAI API key here or as a secret on Streamlit Cloud
openai.api_key = st.secrets["OPENAI_API_KEY"]

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
            prompt = f"""
            You are a helpful assistant that writes 3 creative Instagram captions for the description below.
            Also suggest 5 trending hashtags relevant to the content.

            Description: "{user_input}"
            """
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You create Instagram captions and hashtags."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9,
                    max_tokens=300
                )
                result = response['choices'][0]['message']['content']
                st.success("✅ Captions and hashtags ready:")
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ Error: {e}")
