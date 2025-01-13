from __future__ import annotations
from .card import Card, CardType
from .player import Player
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .game_manager import GameManager

class Rules:
    @staticmethod
    def apply_card_effect(card: Card, game_manager: GameManager):
        if card.card_type == CardType.SKIP:
            game_manager._update_turn()
        
        elif card.card_type == CardType.REVERSE:
            game_manager.direction *= -1
            if len(game_manager.players) == 2:
                game_manager._update_turn()
                
        elif card.card_type == CardType.DRAW_TWO:
            next_player = game_manager.players[
                (game_manager.current_player_index + game_manager.direction) 
                % len(game_manager.players)
            ]
            for _ in range(2):
                next_player.add_card(game_manager.deck.draw_card())
            game_manager._update_turn()
            
        elif card.card_type == CardType.WILD_DRAW_FOUR:
            next_player = game_manager.players[
                (game_manager.current_player_index + game_manager.direction) 
                % len(game_manager.players)
            ]
            for _ in range(4):
                next_player.add_card(game_manager.deck.draw_card())
            game_manager._update_turn()
