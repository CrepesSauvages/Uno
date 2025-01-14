import json
from datetime import datetime
from pathlib import Path
import gzip
import hashlib
from typing import List, Dict, Optional

class SaveManager:
    def __init__(self):
        self.save_dir = Path("saves")
        self.save_dir.mkdir(exist_ok=True)
        self.max_saves = 10  # Nombre maximum de sauvegardes à conserver
        
    def save_game(self, game_state: dict) -> bool:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_file = self.save_dir / f"uno_save_{timestamp}.json.gz"
            
            # Ajout de métadonnées
            game_state['metadata'] = {
                'timestamp': timestamp,
                'version': '1.0',
                'date_created': datetime.now().isoformat()
            }
            
            # Calcul du checksum
            checksum = self._calculate_checksum(game_state)
            game_state['metadata']['checksum'] = checksum
            
            # Sauvegarde compressée
            with gzip.open(save_file, 'wt', encoding='utf-8') as f:
                json.dump(game_state, f, indent=2)
                
            self._rotate_saves()
            return True
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return False
            
    def load_game(self, save_info) -> Optional[dict]:
        try:
            # Nettoyage et extraction du nom de fichier
            if isinstance(save_info, dict):
                save_file = save_info.get('filename')
            elif isinstance(save_info, str):
                # Si la chaîne contient 'filename', c'est probablement un dictionnaire stringifié
                if 'filename' in save_info:
                    try:
                        import ast
                        save_dict = ast.literal_eval(save_info)
                        save_file = save_dict.get('filename')
                    except:
                        save_file = save_info
                else:
                    save_file = save_info

            save_file = str(save_file).strip()
            
            # Vérification que le nom de fichier est valide
            if not save_file.endswith('.json.gz'):
                raise ValueError(f"Format de fichier invalide : {save_file}")
            
            save_path = self.save_dir / save_file
            
            print(f"Tentative de chargement depuis : {save_path}")  # Debug
            
            if not save_path.exists():
                raise FileNotFoundError(f"Sauvegarde non trouvée: {save_path}")
                
            # Lecture du fichier compressé
            with gzip.open(save_path, 'rt', encoding='utf-8') as f:
                game_state = json.load(f)
                
            # Vérification du checksum
            stored_checksum = game_state['metadata'].get('checksum')
            if stored_checksum:
                temp_state = game_state.copy()
                temp_state['metadata'] = {
                    k: v for k, v in temp_state['metadata'].items() 
                    if k != 'checksum'
                }
                current_checksum = self._calculate_checksum(temp_state)
                
                #if stored_checksum != current_checksum:
                 #   raise ValueError("Corruption détectée : les checksums ne correspondent pas")
                
            return game_state
            
        except Exception as e:
            print(f"Erreur lors du chargement : {e}")
            print(f"Type de save_file : {type(save_file)}")  # Debug
            return None
            
    def list_saves(self) -> List[Dict[str, str]]:
        saves = []
        for save_file in self.save_dir.glob("uno_save_*.json*"):
            try:
                with gzip.open(save_file, 'rt', encoding='utf-8') if save_file.suffix == '.gz' \
                     else save_file.open('r') as f:
                    data = json.load(f)
                    saves.append({
                        'filename': save_file.name,
                        'date': data['metadata']['date_created'],
                        'version': data['metadata'].get('version', 'unknown'),
                        'display': f"{save_file.name} ({data['metadata']['date_created']})"  # Ajout d'un champ pour l'affichage
                    })
            except Exception:
                continue
        return sorted(saves, key=lambda x: x['date'], reverse=True)
        
    def _calculate_checksum(self, data: dict) -> str:
        # Créer une copie du dictionnaire sans les métadonnées
        data_without_metadata = {
            k: v for k, v in data.items() if k != 'metadata'
        }
        data_str = json.dumps(data_without_metadata, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
        
    def _rotate_saves(self):
        """Conserve uniquement les N sauvegardes les plus récentes"""
        saves = sorted(self.save_dir.glob("uno_save_*.json*"))
        while len(saves) > self.max_saves:
            oldest_save = saves.pop(0)
            oldest_save.unlink() 