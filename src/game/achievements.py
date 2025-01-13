from typing import Dict, Set

class Achievements:
    def __init__(self):
        self.unlocked: Set[str] = set()
        self.achievements: Dict[str, dict] = {
            'first_win': {
                'name': "Premier Succès",
                'description': "Gagner votre première partie",
                'icon': "🏆"
            },
            'perfect_game': {
                'name': "Partie Parfaite",
                'description': "Gagner sans piocher de carte",
                'icon': "⭐"
            },
            'comeback': {
                'name': "Retour Victorieux",
                'description': "Gagner avec plus de 10 cartes en main",
                'icon': "🔄"
            },
            'special_master': {
                'name': "Maître des Cartes Spéciales",
                'description': "Jouer 5 cartes spéciales dans une partie",
                'icon': "✨"
            }
        }
        
    def check_achievement(self, achievement_id: str, game_state: dict) -> bool:
        if achievement_id in self.unlocked:
            return False
            
        if self._conditions_met(achievement_id, game_state):
            self.unlocked.add(achievement_id)
            return True
        return False
        
    def _conditions_met(self, achievement_id: str, game_state: dict) -> bool:
        if achievement_id == 'first_win':
            return game_state.get('games_won', 0) == 1
        elif achievement_id == 'perfect_game':
            return game_state.get('cards_drawn', 0) == 0
        elif achievement_id == 'comeback':
            return game_state.get('max_cards_in_hand', 0) >= 10
        elif achievement_id == 'special_master':
            return game_state.get('special_cards_played', 0) >= 5
        return False
        
    def display_achievement(self, achievement_id: str):
        achievement = self.achievements[achievement_id]
        print(f"\n🎉 SUCCÈS DÉBLOQUÉ ! 🎉")
        print(f"{achievement['icon']} {achievement['name']}")
        print(f"➤ {achievement['description']}") 