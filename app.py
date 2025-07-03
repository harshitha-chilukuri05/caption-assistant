import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_captions(description):
    prompt = f"""
    You're an expert social media strategist. Generate 3 creative Instagram captions for the following post:

    Description: {description}

    Each caption must:
    - Be short (under 15 words)
    - Include 3-5 trending hashtags
    - Match current Instagram style and vibe
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=250
    )
    
    return response['choices'][0]['message']['content']

st.title("📸 AI Instagram Caption Assistant")
st.write("Upload a photo or describe your post to generate captions & hashtags!")

user_description = st.text_area("Enter a description for your post:")

if st.button("Generate Captions"):
    if user_description.strip():
        with st.spinner("Generating with GPT-4..."):
            captions = generate_captions(user_description)
        st.success("Captions Ready!")
        st.markdown("### 📢 Generated Captions")
        st.markdown(captions)
    else:
        st.warning("Please enter a description to generate captions.")
