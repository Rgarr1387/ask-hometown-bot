
import streamlit as st
import openai
import os

st.set_page_config(page_title="Ask Hometown Bot", page_icon="🦷")
st.title("🦷 Ask Hometown Bot")
st.markdown("Hi there! Ask me anything about Hometown Dental policies, benefits, or procedures.")

# Load content
@st.cache_data
def load_chunks():
    with open("policy_chunks.txt", "r", encoding="utf-8") as f:
        return [chunk.strip() for chunk in f.read().split("-----") if chunk.strip()]

chunks = load_chunks()

# Initialize OpenAI client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def search_chunks(query, chunks):
    prompt = f"""You are a helpful HR assistant. Based on the employee handbook, answer the question:

"{query}"

Here are some relevant policy excerpts:
"""
    top_chunks = chunks[:5]
    prompt += "\n\n".join(top_chunks)
    prompt += "\n\nAnswer the question clearly and briefly."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Ask box
user_question = st.text_input("What would you like to know?")
if user_question:
    with st.spinner("Searching the handbook..."):
        answer = search_chunks(user_question, chunks)
        st.markdown("### 📝 Answer")
        st.write(answer)
