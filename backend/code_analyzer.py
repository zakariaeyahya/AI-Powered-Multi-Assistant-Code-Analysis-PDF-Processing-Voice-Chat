import os
import subprocess
import sys
import tempfile
import venv
from langchain_groq import ChatGroq

def create_virtual_env(env_path):
    venv.create(env_path, with_pip=True)

def get_activate_script(env_path):
    if sys.platform == 'win32':
        return os.path.join(env_path, 'Scripts', 'activate.bat')
    else:
        return os.path.join(env_path, 'bin', 'activate')

def run_in_virtual_env(env_path, command):
    activate_script = get_activate_script(env_path)
    if sys.platform == 'win32':
        cmd = f'call "{activate_script}" && {command}'
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        cmd = f'source "{activate_script}" && {command}'
        return subprocess.run(cmd, shell=True, executable='/bin/bash', capture_output=True, text=True)

def install_requirements(env_path, requirements_file):
    result = run_in_virtual_env(env_path, f'pip install -r "{requirements_file}"')
    if result.returncode != 0:
        raise Exception(f"Erreur lors de l'installation des dépendances : {result.stderr}")

def run_python_file(env_path, file_path):
    result = run_in_virtual_env(env_path, f'python "{file_path}"')
    return result.stdout, result.stderr

def analyze_with_llama(code, output, error):
    groq_api_key = os.getenv("api_groq")  # Utilisez une variable d'environnement pour la clé API
    llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0, groq_api_key=groq_api_key)
    
    prompt = f"""
    Analysez le code Python suivant et ses résultats d'exécution :

    Code :
    ```python
    {code}
    ```

    Sortie standard :
    {output}

    Erreurs (le cas échéant) :
    {error}

    Veuillez fournir une analyse détaillée du code, y compris :
    1. Si le code s'est exécuté avec succès ou s'il y a eu des erreurs.
    2. Une explication des erreurs éventuelles et des suggestions pour les corriger.
    3. Des recommandations pour améliorer le code ou sa performance.
    4. Toute autre observation pertinente.

    Répondez en français.
    """

    response = llm.invoke(prompt)
    return response.content

def test_python_file(file_path, requirements_file=None):
    with tempfile.TemporaryDirectory() as temp_dir:
        env_path = os.path.join(temp_dir, 'venv')
        
        try:
            create_virtual_env(env_path)

            if requirements_file:
                install_requirements(env_path, requirements_file)

            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()

            output, error = run_python_file(env_path, file_path)

            if error:
                return error
            else:
                analysis = analyze_with_llama(code, output, error)
                return analysis
        
        except Exception as e:
            return str(e)
