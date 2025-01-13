from typing import List
from .player import Player
from .deck import Deck
from .card import Card, Color, CardType
from ..ui.console_ui import ConsoleUI
from .rules import Rules
from .save_manager import SaveManager
from .achievements import Achievements
import json

class GameManager:
    def __init__(self, difficulty: str):
        self.difficulty = difficulty
        self.deck = Deck()
        self.players: List[Player] = []
        self.current_player_index = 0
        self.direction = 1  # 1 pour sens horaire, -1 pour anti-horaire
        self.ui = ConsoleUI()
        self._initialize_players()
        self.scores = {player.name: 0 for player in self.players}
        self.save_manager = SaveManager()
        self.achievements = Achievements()
        self.game_stats = {
            'cards_played': 0,
            'turns_played': 0,
            'cards_drawn': 0,
            'special_cards_played': 0,
            'games_won': 0,
            'max_cards_in_hand': 0
        }
        
    def _initialize_players(self):
        self.players = [
            Player("Joueur", False),
            Player("IA 1", True),
            Player("IA 2", True),
            Player("IA 3", True)
        ]
        
    def start_game(self):
        self.ui.animate_shuffle()
        self.deck.shuffle()
        # Distribution des cartes
        for _ in range(7):
            for player in self.players:
                player.add_card(self.deck.draw_card())
        
        # Première carte
        initial_card = self.deck.draw_card()
        while initial_card.color == Color.BLACK:
            self.deck.cards.append(initial_card)
            initial_card = self.deck.draw_card()
        self.deck.discard_pile.append(initial_card)
        
    def play_turn(self):
        current_player = self.players[self.current_player_index]
        top_card = self.deck.discard_pile[-1]
        
        self.ui.display_game_state(current_player, top_card, self)
        
        if current_player.is_ai:
            self._play_ai_turn(current_player)
        else:
            self._play_human_turn(current_player)
            
        self._update_turn()
        
    def _update_turn(self):
        self.current_player_index = (
            self.current_player_index + self.direction
        ) % len(self.players)
        
    def is_game_over(self) -> bool:
        return any(len(player.hand) == 0 for player in self.players)

    def _play_ai_turn(self, player: Player):
        top_card = self.deck.discard_pile[-1]
        playable_cards = [
            card for card in player.hand 
            if card.can_be_played_on(top_card)
        ]
        
        if not playable_cards:
            drawn_card = self.deck.draw_card()
            player.add_card(drawn_card)
            if drawn_card.can_be_played_on(top_card):
                self._play_card(player, drawn_card)
            return
            
        if self.difficulty == "facile":
            card_to_play = playable_cards[0]
        else:
            card_to_play = self._choose_strategic_card(player, playable_cards)
            
        self._play_card(player, card_to_play)
        
    def _choose_strategic_card(self, player: Player, playable_cards: List[Card]) -> Card:
        # Stratégie pour difficulté moyenne et difficile
        # Priorité aux cartes spéciales
        special_cards = [c for c in playable_cards if c.card_type != CardType.NUMBER]
        if special_cards and self.difficulty == "difficile":
            return special_cards[0]
            
        # Jouer les cartes de même couleur en priorité
        top_card = self.deck.discard_pile[-1]
        same_color_cards = [c for c in playable_cards if c.color == top_card.color]
        if same_color_cards:
            return same_color_cards[0]
            
        return playable_cards[0]
        
    def _play_card(self, player: Player, card: Card):
        self.ui.animate_card_play(card)
        player.remove_card(card)
        
        if len(player.hand) == 1:
            self.ui.animate_uno_call(player.name)
            
        if card.card_type != CardType.NUMBER:
            self.ui.animate_card_effect(card.card_type)
            
        self.deck.discard_pile.append(card)
        self.game_stats['cards_played'] += 1
        
        if card.card_type != CardType.NUMBER:
            self.game_stats['special_cards_played'] += 1
            self._check_special_master_achievement()
            
        # Mettre à jour le nombre maximum de cartes en main
        for p in self.players:
            self.game_stats['max_cards_in_hand'] = max(
                self.game_stats['max_cards_in_hand'], 
                len(p.hand)
            )
            
        if card.color == Color.BLACK:
            if player.is_ai:
                # L'IA choisit la couleur la plus présente dans sa main
                colors = [c.color for c in player.hand if c.color != Color.BLACK]
                if colors:
                    most_common_color = max(set(colors), key=colors.count)
                    card.color = most_common_color
                else:
                    card.color = Color.RED
            else:
                new_color = self.ui.get_color_choice()
                card.color = new_color
                
        Rules.apply_card_effect(card, self)
        
    def _play_human_turn(self, player: Player):
        while True:
            choice = self.ui.get_player_move(player, self.deck.discard_pile[-1])
            
            if choice == -4:  # Quitter
                self.quit_game = True
                return
                
            if choice == -2:  # Sauvegarder
                if self.save_current_game():
                    self.ui.show_message("Partie sauvegardée avec succès !")
                else:
                    self.ui.show_message("Erreur lors de la sauvegarde !", error=True)
                continue
            
            if choice == -1:  # Piocher une carte
                drawn_card = self.deck.draw_card()
                player.add_card(drawn_card)
                self.ui.display_game_state(player, self.deck.discard_pile[-1], self)
                
                if drawn_card.can_be_played_on(self.deck.discard_pile[-1]):
                    if self.ui.ask_play_drawn_card():
                        self._play_card(player, drawn_card)
                break
            else:
                card_to_play = player.hand[choice]
                self._play_card(player, card_to_play)
                break

    def calculate_round_score(self, winner: Player) -> int:
        score = 0
        for player in self.players:
            if player != winner:
                for card in player.hand:
                    if card.card_type == CardType.NUMBER:
                        score += card.value
                    elif card.card_type in [CardType.SKIP, CardType.REVERSE, CardType.DRAW_TWO]:
                        score += 20
                    else:  # WILD et WILD_DRAW_FOUR
                        score += 50
        return score
        
    def end_game(self):
        winner = next(player for player in self.players if len(player.hand) == 0)
        self.ui.animate_win(winner.name)
        round_score = self.calculate_round_score(winner)
        self.scores[winner.name] += round_score
        
        # Mettre à jour les statistiques
        self.game_stats['games_won'] += 1
        
        # Vérifier les achievements
        self._check_achievements(winner)
        
        self.ui.announce_winner(winner, round_score, self.scores)
        
    def _check_achievements(self, winner: Player):
        # Premier succès
        if self.achievements.check_achievement('first_win', self.game_stats):
            self.ui.display_achievement('first_win')
            
        # Partie parfaite
        if self.game_stats['cards_drawn'] == 0:
            if self.achievements.check_achievement('perfect_game', self.game_stats):
                self.ui.display_achievement('perfect_game')
                
        # Retour victorieux
        if self.game_stats['max_cards_in_hand'] >= 10:
            if self.achievements.check_achievement('comeback', self.game_stats):
                self.ui.display_achievement('comeback')
                
    def _check_special_master_achievement(self):
        if self.game_stats['special_cards_played'] >= 5:
            if self.achievements.check_achievement('special_master', self.game_stats):
                self.ui.display_achievement('special_master')
                
    def save_current_game(self) -> bool:
        try:
            game_state = {
                'difficulty': self.difficulty,
                'current_player': self.current_player_index,
                'direction': self.direction,
                'scores': self.scores,
                'stats': self.game_stats,
                'players': [
                    {
                        'name': player.name,
                        'is_ai': player.is_ai,
                        'hand': [
                            {
                                'color': card.color.value,
                                'type': card.card_type.value,
                                'value': card.value
                            } for card in player.hand
                        ]
                    } for player in self.players
                ],
                'discard_pile': [
                    {
                        'color': card.color.value,
                        'type': card.card_type.value,
                        'value': card.value
                    } for card in self.deck.discard_pile
                ],
                'achievements': list(self.achievements.unlocked),
                'game_stats': self.game_stats
            }
            
            self.save_manager.save_game(game_state)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return False

    def load_game(self, save_file: str) -> bool:
        try:
            game_state = self.save_manager.load_game(save_file)
            
            # Restaurer l'état du jeu
            self.difficulty = game_state['difficulty']
            self.current_player_index = game_state['current_player']
            self.direction = game_state['direction']
            self.scores = game_state['scores']
            self.game_stats = game_state['stats']
            
            # Recréer les joueurs et leurs mains
            self.players = []
            for player_data in game_state['players']:
                player = Player(player_data['name'], player_data['is_ai'])
                for card_data in player_data['hand']:
                    card = Card(
                        Color(card_data['color']),
                        CardType(card_data['type']),
                        card_data.get('value')
                    )
                    player.add_card(card)
                self.players.append(player)
            
            # Recréer la pile de défausse
            self.deck = Deck()
            self.deck.discard_pile = []
            for card_data in game_state['discard_pile']:
                card = Card(
                    Color(card_data['color']),
                    CardType(card_data['type']),
                    card_data.get('value')
                )
                self.deck.discard_pile.append(card)
                
            # Charger les achievements
            self.achievements.unlocked = set(game_state.get('achievements', []))
            self.game_stats = game_state.get('game_stats', {
                'cards_played': 0,
                'turns_played': 0,
                'cards_drawn': 0,
                'special_cards_played': 0,
                'games_won': 0,
                'max_cards_in_hand': 0
            })
            
            return True
        except Exception as e:
            print(f"Erreur lors du chargement : {e}")
            return False
