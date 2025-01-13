import sys
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir) 