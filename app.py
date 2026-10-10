import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

st.title("Atendente")

if "pergunta" not in st.session_state:
    st.session_state.pergunta = None
    st.session_state.resposta = None

if st.session_state.resposta is not None:
    with st.container(border=True):
        st.markdown(f"**Você:** {st.session_state.pergunta}")
        st.markdown(st.session_state.resposta)

with st.form("form_pergunta", clear_on_submit=True):
    pergunta = st.text_input("Sua pergunta")
    enviado = st.form_submit_button("Enviar")

if enviado and pergunta:
    with st.spinner("Pensando..."):
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "Você é um atendente"},
                {"role": "user", "content": pergunta},
            ],
        )
    st.session_state.pergunta = pergunta
    st.session_state.resposta = response.choices[0].message.content
    st.rerun()
