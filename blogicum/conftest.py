import sys
from pathlib import Path

# Добавляем текущую директорию (blogicum корень с manage.py) в PATH
sys.path.insert(0, str(Path(__file__).parent))
