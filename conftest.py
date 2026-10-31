# conftest.py
import os
import sys

# Добавляем корневую папку проекта в sys.path, 
# чтобы pytest видел модули parsers и pipeline
sys.path.insert(0, os.path.dirname(__file__))