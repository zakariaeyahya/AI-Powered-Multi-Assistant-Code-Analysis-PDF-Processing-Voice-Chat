import streamlit as st
import requests
import tempfile
import os

# Configuration de la page Streamlit
st.set_page_config(page_title="Analyseur de Code Python, PDF et Assistant IA", layout="wide")

# Initialisation des variables de session
if 'code' not in st.session_state:
    st.session_state.code = ""
if 'pdf_text' not in st.session_state:
    st.session_state.pdf_text = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {"code": [], "general": [], "pdf": []}

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

# Fonction pour effacer l'historique
def clear_history(assistant_type):
    response = send_request("clear_history", data={"assistant_type": assistant_type})
    if response and response.get('message'):
        st.success(response['message'])
        st.session_state.chat_history[assistant_type] = []
        st.experimental_rerun()
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

    # Faire défiler automatiquement vers le bas
    st.markdown('<script>window.scrollTo(0,document.body.scrollHeight);</script>', unsafe_allow_html=True)

# Page d'analyse de code et assistant code
def code_analysis_and_assistant_page():
    st.title("Analyse de Code Python et Assistant Code")

    # Analyse de code
    st.header("Analyse de Code")
    uploaded_file = st.file_uploader("Choisissez un fichier Python", type="py")

    if uploaded_file is not None:
        st.write("Fichier chargé :", uploaded_file.name)
        
        if st.button("Analyser et Corriger"):
            with st.spinner("Analyse en cours..."):
                files = {'file': uploaded_file}
                result = send_request("analyze", files=files)
                
                if result:
                    if result.get('error'):
                        st.error("Erreur détectée :")
                        st.code(result['error'])
                        st.write("Code corrigé :")
                        st.code(result['corrected_code'])
                        st.session_state.code = result['corrected_code']
                    else:
                        st.success("Aucune erreur détectée.")
                        st.write("Analyse du code :")
                        st.write(result['analysis'])
                        st.session_state.code = result['original_code']

    # Assistant Code
    if st.session_state.code:
        st.write("Code actuel :")
        st.code(st.session_state.code, language="python")
        display_chat_and_handle_questions("code", st.session_state.code)
    else:
        st.warning("Veuillez d'abord charger et analyser un fichier Python pour pouvoir poser des questions sur le code.")

# Page d'assistant général
def assistant_general_page():
    st.title("Assistant Général")
    display_chat_and_handle_questions("general")

# Page d'analyse de PDF et assistant PDF
def pdf_analysis_and_assistant_page():
    st.title("Analyse de PDF et Assistant PDF")

    # Analyse de PDF
    st.header("Analyse de PDF")
    uploaded_file = st.file_uploader("Choisissez un fichier PDF", type="pdf")

    if uploaded_file is not None:
        st.write("Fichier chargé :", uploaded_file.name)
        
        if st.button("Analyser le PDF"):
            with st.spinner("Analyse en cours..."):
                files = {'file': uploaded_file}
                result = send_request("analyze_pdf", files=files)
                
                if result and result.get('pdf_text'):
                    st.success("PDF analysé avec succès.")
                    st.session_state.pdf_text = result['pdf_text']
                    st.text_area("Aperçu du contenu du PDF :", value=result['pdf_text'][:1000] + "...", height=200)
                    
                    st.subheader("Métadonnées du PDF")
                    metadata = result.get('metadata', {})
                    for key, value in metadata.items():
                        st.write(f"{key}: {value}")
                    
                    st.subheader("Informations supplémentaires")
                    st.write(f"Nombre de pages : {result.get('page_count', 0)}")
                else:
                    st.error("Erreur lors de l'analyse du PDF.")

    # Assistant PDF
    if st.session_state.pdf_text:
        display_chat_and_handle_questions("pdf", st.session_state.pdf_text)
    else:
        st.warning("Veuillez d'abord charger et analyser un fichier PDF pour pouvoir poser des questions sur son contenu.")

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
