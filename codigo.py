import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
modelo_ia = OpenAI(
    api_key=os.getenv("TOKEN_GEMINI"),
    base_url="https://generativelanguage.googleapis.com/v1beta",)

#instalar a biblioteca streamlit-chat 
# py -m pip install streamlit openai

#Rodar o comando no terminal: 
# py -m streamlit run codigo.py

st.write("## Stella - ChatBot de IA")

# Criar histórico de mensagens na sessão do Streamlit
if not "lista_mensagens" in st.session_state:
    st.session_state["lista_mensagens"] = []

# Campo de entrada para o usuário digitar a mensagem 
mensagem_usuario = st.text_input("Escreva sua mensagem aqui:")
arquivo = st.file_uploader("Faça upload de um arquivo (opcional):", type=["txt", "pdf", "docx", "png", "jpg", "jpeg"])

for mensagem in st.session_state["lista_mensagens"]:
    quem_enviou = mensagem["role"]
    texto_mensagem = mensagem["content"]
    st.chat_message(quem_enviou).write(texto_mensagem)

if mensagem_usuario:

    # Adiciona a mensagem do usuário à lista de mensagens
    st.chat_message("user").write(mensagem_usuario)
    mensagem1 = {"role": "user", "content": mensagem_usuario}    
    st.session_state["lista_mensagens"].append(mensagem1)

    # Resposta do assistente (IA)
    resposta_modelo = modelo_ia.chat.completions.create(
        messages=st.session_state["lista_mensagens"],
        model="gemini-flash-lite-latest",
    )

    print(resposta_modelo)

    resposta_ia = resposta_modelo.choices[0].message.content

    # Enviar resposta (IA) para o chat
    st.chat_message("assistant").write(resposta_ia)
    mensagem2 = {"role": "assistant", "content": resposta_ia}
    st.session_state["lista_mensagens"].append(mensagem2)

