import streamlit as st
import requests
import tempfile
import os
# Fonction pour effacer l'historique
from streamlit.runtime.scriptrunner import RerunException
from streamlit.runtime.scriptrunner import RerunData

# Configuration de la page Streamlit
st.set_page_config(page_title="Analyseur de Code Python, PDF et Assistant IA", layout="wide")

# Initialisation des variables de session
if 'code' not in st.session_state:
    st.session_state.code = ""
if 'pdf_text' not in st.session_state:
    st.session_state.pdf_text = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {"code": [], "general": [], "pdf": []}
def clear_history(assistant_type):
    response = send_request("clear_history", data={"assistant_type": assistant_type})
    if response and response.get('message'):
        st.success(response['message'])
        st.session_state.chat_history[assistant_type] = []
        st.experimental_rerun()
    else:
        st.error("Erreur lors de l'effacement de l'historique")

# Dans la fonction où le bouton d'effacement est défini

# Fonction pour envoyer une requête au backend
def send_request(endpoint, data=None, files=None):
    try:
        url = f"http://localhost:8000/{endpoint}"
        if files:
            response = requests.post(url, files=files)
        elif data:
            response = requests.post(url, json=data)
        else:
            response = requests.post(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erreur de communication avec le serveur: {str(e)}")
        return None



def clear_history(assistant_type):
    response = send_request("clear_history", data={"assistant_type": assistant_type})
    if response and response.get('message'):
        st.success(response['message'])
        st.session_state.chat_history[assistant_type] = []
        st.rerun()
    else:
        st.error("Erreur lors de l'effacement de l'historique")

# Fonction générique pour afficher le chat et gérer les questions
def display_chat_and_handle_questions(assistant_type, content=""):
    st.header(f"Assistant {assistant_type.capitalize()}")

    # Créer un conteneur pour l'historique du chat
    chat_container = st.container()

    # Zone de saisie (en bas)
    user_question = st.text_input(f"Poser une question sur {assistant_type}", key=f"input_{assistant_type}")
    send_button = st.button("Envoyer", key=f"send_{assistant_type}_question")

    if send_button and user_question:
        # Ajouter la question de l'utilisateur à l'historique
        st.session_state.chat_history[assistant_type].append(("user", user_question))
        
        # Obtenir la réponse de l'assistant
        with st.spinner(f"L'assistant {assistant_type} réfléchit..."):
            chat_response = send_request("chat", data={
                "message": user_question,
                "content": content,
                "assistant_type": assistant_type
            })
            if chat_response:
                assistant_response = chat_response['response']
                st.session_state.chat_history[assistant_type].append(("assistant", assistant_response))

    # Afficher l'historique du chat dans le conteneur
    with chat_container:
        for role, message in st.session_state.chat_history[assistant_type]:
            with st.chat_message(role):
                st.write(message)

    # Bouton pour effacer l'historique du chat
    if st.button(f"Effacer l'historique du chat {assistant_type}"):
        clear_history(assistant_type)
        raise RerunException(RerunData())
        # Faire défiler automatiquement vers le bas
    st.markdown('<script>window.scrollTo(0,document.body.scrollHeight);</script>', unsafe_allow_html=True)

# Page d'analyse de code et assistant code
def code_analysis_and_assistant_page():
    st.title("Analyse de Code Python et Assistant Code")
    # Analyse de code
    st.header("Analyse de Code")
    uploaded_files = st.file_uploader("Choisissez un ou plusieurs fichiers Python", type="py", accept_multiple_files=True)
    requirements_file = st.file_uploader("Choisissez le fichier requirements.txt", type="txt", accept_multiple_files=False)

    if uploaded_files and requirements_file:
        for uploaded_file in uploaded_files:
            st.write("Fichier chargé :", uploaded_file.name)

        if st.button("Analyser et Corriger"):
            for uploaded_file in uploaded_files:
                with st.spinner(f"Analyse en cours pour {uploaded_file.name}..."):
                    files = {'file': uploaded_file, 'requirements_file': requirements_file}
                    result = send_request("analyze", files=files)

                    if result:
                        st.subheader(f"Résultats pour {uploaded_file.name}")
                        if result.get('error'):
                            st.error("Erreur détectée :")
                            st.code(result['error'])
                            st.write("Code corrigé :")
                            st.code(result['corrected_code'])
                        else:
                            st.success("Aucune erreur détectée.")
                            st.write("Analyse du code :")
                            st.write(result['analysis'])

                        st.session_state.code += f"\n\n# Fichier: {uploaded_file.name}\n{result.get('original_code', '')}"
        # Assistant Code
    if st.session_state.code:
        st.write("Code actuel :")
        st.code(st.session_state.code, language="python")
        display_chat_and_handle_questions("code", st.session_state.code)
    else:
        st.warning("Veuillez d'abord charger et analyser un ou plusieurs fichiers Python pour pouvoir poser des questions sur le code.")

# Page d'assistant général
def assistant_general_page():
    st.title("Assistant Général")
    display_chat_and_handle_questions("general")

def pdf_analysis_and_assistant_page():
    st.title("Analyse de PDF et Assistant PDF")

    # Analyse de PDF
    st.header("Analyse de PDF")
    uploaded_files = st.file_uploader("Choisissez un ou plusieurs fichiers PDF", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.write("Fichier chargé :", uploaded_file.name)

        if st.button("Analyser les PDFs"):
            for uploaded_file in uploaded_files:
                with st.spinner(f"Analyse en cours pour {uploaded_file.name}..."):
                    files = {'file': uploaded_file}
                    result = send_request("analyze_pdf", files=files)

                    if result and result.get('pdf_text'):
                        st.subheader(f"Résultats pour {uploaded_file.name}")
                        st.success("PDF analysé avec succès.")
                        st.session_state.pdf_text = result['pdf_text']
                    else:
                        st.error(f"Erreur lors de l'analyse du PDF {uploaded_file.name}.")
                        st.session_state.pdf_text = ""

        display_chat_and_handle_questions("pdf", st.session_state.pdf_text)
    else:
        st.warning("Aucun PDF n'a été chargé avec succès.")
# Définition des pages
pages = {
    "Analyse de Code et Assistant Code": code_analysis_and_assistant_page,
    "Analyse de PDF et Assistant PDF": pdf_analysis_and_assistant_page,
    "Assistant Général": assistant_general_page
}

# Navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Aller à", list(pages.keys()))
pages[selection]()
