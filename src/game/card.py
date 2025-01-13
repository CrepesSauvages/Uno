from enum import Enum

class Color(Enum):
    RED = "rouge"
    BLUE = "bleu"
    GREEN = "vert"
    YELLOW = "jaune"
    BLACK = "noir"  # Pour les cartes +4 et Joker

class CardType(Enum):
    NUMBER = "nombre"
    SKIP = "passer"
    REVERSE = "inverse"
    DRAW_TWO = "+2"
    WILD = "joker"
    WILD_DRAW_FOUR = "+4"

class Card:
    def __init__(self, color: Color, card_type: CardType, value: int = None):
        self.color = color
        self.card_type = card_type
        self.value = value  # None pour les cartes spéciales
        
    def __str__(self):
        if self.card_type == CardType.NUMBER:
            return f"{self.color.value} {self.value}"
        return f"{self.color.value} {self.card_type.value}"
        
    def can_be_played_on(self, other_card: 'Card') -> bool:
        if self.color == Color.BLACK:  # Joker et +4 peuvent toujours être joués
            return True
        return (self.color == other_card.color or 
                (self.card_type == other_card.card_type and 
                 self.card_type != CardType.NUMBER) or
                (self.card_type == CardType.NUMBER and 
                 other_card.card_type == CardType.NUMBER and 
                 self.value == other_card.value))
