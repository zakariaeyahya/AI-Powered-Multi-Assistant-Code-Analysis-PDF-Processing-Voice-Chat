from .main import app
from .code_analyzer import test_python_file
from .code_corrector import correct_python_file
from backend import app, test_python_file, correct_python_file
__all__ = ['app', 'test_python_file', 'correct_python_file']