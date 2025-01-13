import json
from datetime import datetime
from pathlib import Path

class SaveManager:
    def __init__(self):
        self.save_dir = Path("saves")
        self.save_dir.mkdir(exist_ok=True)
        
    def save_game(self, game_state: dict):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_file = self.save_dir / f"uno_save_{timestamp}.json"
        
        with save_file.open('w') as f:
            json.dump(game_state, f, indent=2)
            
    def load_game(self, save_file: str) -> dict:
        save_path = self.save_dir / save_file
        if not save_path.exists():
            raise FileNotFoundError("Sauvegarde non trouvée")
            
        with save_path.open('r') as f:
            return json.load(f)
            
    def list_saves(self) -> list:
        return [f.name for f in self.save_dir.glob("uno_save_*.json")] 