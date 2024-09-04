import re
from langchain_groq import ChatGroq
import os

def correct_python_file(file_path, error_message):
    # Lire le contenu du fichier
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    os.environ["GROQ_API_KEY"] = "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"
    groq_api_key=os.environ["GROQ_API_KEY"]
    # Créer une instance de ChatGroq avec la clé API fournie
    llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0, groq_api_key=groq_api_key)

    # Préparer le prompt pour la correction
    prompt = f"""
    Voici un extrait de code Python qui contient une erreur :

    ```python
    {code}
    ```

    L'erreur signalée est :
    {error_message}

    Veuillez corriger le code pour résoudre cette erreur. Fournissez uniquement le code corrigé, sans explications supplémentaires.
    """

    # Obtenir la réponse du modèle
    response = llm.invoke(prompt)

    # Extraire le code corrigé de la réponse
    corrected_code = re.search(r'```python\n(.*?)\n```', response.content, re.DOTALL)
    if corrected_code:
        return corrected_code.group(1)
    else:
        return "Impossible d'extraire le code corrigé de la réponse."