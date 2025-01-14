import os
import time
import sys
import random
from colorama import init, Fore, Back, Style
from ..game.card import Card, Color, CardType
from ..game.player import Player
from typing import TYPE_CHECKING, List, Dict, Optional
from datetime import datetime

if TYPE_CHECKING:
    from ..game.game_manager import GameManager

class ConsoleUI:
    def __init__(self):
        init()  # Initialisation de colorama
        self.color_map = {
            Color.RED: Fore.RED,
            Color.BLUE: Fore.BLUE,
            Color.GREEN: Fore.GREEN,
            Color.YELLOW: Fore.YELLOW,
            Color.BLACK: Fore.WHITE
        }
        self.animation_enabled = False
        self.animation_speed = 0.05

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _hide_cursor(self):
        print('\033[?25l', end='')

    def _show_cursor(self):
        print('\033[?25h', end='')

    def _format_card(self, card: Card) -> str:
        color = self.color_map[card.color]
        if card.card_type == CardType.NUMBER:
            return f"{color}[{card.color.value} {card.value}]{Style.RESET_ALL}"
        return f"{color}[{card.color.value} {card.card_type.value}]{Style.RESET_ALL}"

    def display_game_state(self, current_player: Player, top_card: Card, game_manager: 'GameManager'):
        self._clear_screen()
        
        # Bannière décorative
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{' '*25}UNO GAME{' '*25}")
        print(f"{'='*60}{Style.RESET_ALL}\n")

        # Informations sur les autres joueurs
        print(f"{Fore.YELLOW}État des joueurs:{Style.RESET_ALL}")
        for player in game_manager.players:
            cards_count = len(player.hand)
            if player == current_player:
                print(f"> {player.name}: {cards_count} cartes")
            else:
                print(f"  {player.name}: {cards_count} cartes")

        # Carte visible
        print(f"\n{Fore.CYAN}Carte visible :{Style.RESET_ALL}")
        print(f"╔════════════╗")
        print(f"║ {self._format_card(top_card)} ║")
        print(f"╚════════════╝")

        # Main du joueur actuel
        if not current_player.is_ai:
            print(f"\n{Fore.GREEN}Vos cartes :{Style.RESET_ALL}")
            print("╔════════════╗")
            for i, card in enumerate(current_player.hand):
                print(f"║ {i+1}. {self._format_card(card)} ║")
            print("╚════════════╝")

    def get_player_move(self, player: Player, top_card: Card) -> int:
        print(f"\n{Fore.CYAN}Actions disponibles:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}0.{Style.RESET_ALL} Piocher une carte")
        print(f"{Fore.YELLOW}1-{len(player.hand)}.{Style.RESET_ALL} Jouer une carte")
        print(f"{Fore.YELLOW}Commandes spéciales:{Style.RESET_ALL}")
        print("  !save    - Sauvegarder la partie")
        print("  !stats   - Voir les statistiques")
        print("  !help    - Voir l'aide")
        print("  !quit    - Quitter la partie")
        
        while True:
            choice = input(f"\n{Fore.GREEN}Votre choix :{Style.RESET_ALL} ").strip()
            
            if choice.startswith('!'):
                return self._handle_special_command(choice)
            
            try:
                index = int(choice) - 1
                if index == -1:
                    return -1
                if 0 <= index < len(player.hand):
                    if player.hand[index].can_be_played_on(top_card):
                        return index
                    print(f"{Fore.RED}❌ Cette carte ne peut pas être jouée !{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Numéro de carte invalide !{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}❌ Entrée invalide !{Style.RESET_ALL}")

    def get_color_choice(self) -> Color:
        colors = {
            "1": Color.RED,
            "2": Color.BLUE,
            "3": Color.GREEN,
            "4": Color.YELLOW
        }
        
        print(f"\n{Fore.CYAN}Choisissez une couleur :{Style.RESET_ALL}")
        print(f"{Fore.RED}1. Rouge{Style.RESET_ALL}")
        print(f"{Fore.BLUE}2. Bleu{Style.RESET_ALL}")
        print(f"{Fore.GREEN}3. Vert{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}4. Jaune{Style.RESET_ALL}")
        
        while True:
            choice = input(f"\n{Fore.GREEN}Votre choix (1-4) :{Style.RESET_ALL} ")
            if choice in colors:
                return colors[choice]
            print(f"{Fore.RED}❌ Choix invalide !{Style.RESET_ALL}")

    def ask_play_drawn_card(self) -> bool:
        while True:
            choice = input(f"\n{Fore.CYAN}Voulez-vous jouer la carte piochée ? (o/n) :{Style.RESET_ALL} ")
            if choice.lower() in ['o', 'n']:
                return choice.lower() == 'o'
            print(f"{Fore.RED}❌ Réponse invalide, veuillez répondre par 'o' ou 'n'{Style.RESET_ALL}")

    def announce_winner(self, winner: Player, round_score: int, total_scores: dict):
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"{' '*20}🎉 FIN DE LA PARTIE 🎉")
        print(f"\n{Fore.GREEN}Le gagnant est : {winner.name} !{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Points gagnés cette manche : {round_score}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}Tableau des scores :{Style.RESET_ALL}")
        print("╔════════════════════════════════╗")
        for player, score in total_scores.items():
            print(f"║ {player:15s} : {score:10d} ║")
        print("╚════════════════════════════════╝")

    def display_winner(self, player: Player):
        self.announce_winner(player)

    def display_statistics(self, game_stats: dict):
        print(f"\n{Fore.CYAN}📊 Statistiques de la partie :{Style.RESET_ALL}")
        print("╔════════════════════════════════╗")
        print(f"║ Cartes jouées : {game_stats['cards_played']:14d} ║")
        print(f"║ Tours joués   : {game_stats['turns_played']:14d} ║")
        print(f"║ Cartes piochées : {game_stats['cards_drawn']:11d} ║")
        print("╚════════════════════════════════╝")

    def show_message(self, message: str, error: bool = False):
        """Affiche un message à l'utilisateur"""
        color = '\033[91m' if error else '\033[92m'  # Rouge pour erreur, vert pour succès
        print(f"{color}{message}\033[0m")

    def show_saves(self, saves: list):
        print(f"\n{Fore.CYAN}Sauvegardes disponibles :{Style.RESET_ALL}")
        print("╔════════════════════════════════╗")
        for i, save in enumerate(saves, 1):
            print(f"║ {i}. {save}")
        print("╚════════════════════════════════╝")

    def choose_save_file(self, saves: list) -> str:
        self.show_saves(saves)
        while True:
            try:
                choice = input(f"\n{Fore.GREEN}Choisissez une sauvegarde (0 pour annuler) : {Style.RESET_ALL}")
                if choice == "0":
                    return None
                index = int(choice) - 1
                if 0 <= index < len(saves):
                    return saves[index]
                print(f"{Fore.RED}Choix invalide !{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Entrée invalide !{Style.RESET_ALL}")

    def _handle_special_command(self, command: str) -> int:
        if command == "!save":
            return -2  # Code spécial pour la sauvegarde
            
        elif command == "!stats":
            self.display_statistics({
                'cards_played': 0,  # À remplacer par les vraies stats
                'turns_played': 0,
                'cards_drawn': 0
            })
            return -3  # Continue le tour
            
        elif command == "!help":
            self._display_help()
            return -3  # Continue le tour
            
        elif command == "!quit":
            if self._confirm_quit():
                return -4 
            
        print(f"{Fore.RED}Commande non reconnue !{Style.RESET_ALL}")
        return -3  # Continue le tour
        
    def _display_help(self):
        print(f"\n{Fore.CYAN}=== AIDE ===")
        print("Commandes disponibles :")
        print("0          - Piocher une carte")
        print("1-N        - Jouer la carte correspondante")
        print("!save      - Sauvegarder la partie")
        print("!stats     - Voir les statistiques")
        print("!help      - Afficher cette aide")
        print("!quit      - Quitter la partie")
        print(f"============{Style.RESET_ALL}\n")
        
    def _confirm_quit(self) -> bool:
        while True:
            choice = input(f"{Fore.YELLOW}Voulez-vous vraiment quitter ? (o/n) : {Style.RESET_ALL}")
            if choice.lower() == 'o':
                return True
            if choice.lower() == 'n':
                return False

    def animate_card_play(self, card: Card):
        if not self.animation_enabled:
            return
            
        card_str = self._format_card(card)
        frames = [
            f"┌─────────┐",
            f"│{' ' * 9}│",
            f"│   {card_str}   │",
            f"│{' ' * 9}│",
            f"└─────────┘"
        ]
        
        # Animation de la carte qui "tombe"
        height = 10
        for i in range(height):
            self._clear_screen()
            print('\n' * (height - i))
            for frame in frames:
                print(frame)
            time.sleep(self.animation_speed)
            
    def animate_shuffle(self):
        if not self.animation_enabled:
            return
            
        self._hide_cursor()
        cards = ["🂠", "🂡", "🂢", "🂣", "🂤", "🂥", "🂦"]
        width = 20
        
        for _ in range(3):  # 3 animations de mélange
            for i in range(width):
                sys.stdout.write("\r" + " " * width)
                sys.stdout.write("\r")
                for j in range(width):
                    if j == i:
                        sys.stdout.write(random.choice(cards))
                    else:
                        sys.stdout.write(" ")
                sys.stdout.flush()
                time.sleep(self.animation_speed)
        print("\n")
        self._show_cursor()
        
    def animate_uno_call(self, player_name: str):
        if not self.animation_enabled:
            return
            
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE]
        uno_text = "UNO!"
        
        self._hide_cursor()
        for _ in range(5):
            for color in colors:
                sys.stdout.write("\r" + " " * 40)
                sys.stdout.write("\r")
                sys.stdout.write(f"{color}{player_name} dit {uno_text}!{Style.RESET_ALL}")
                sys.stdout.flush()
                time.sleep(0.2)
        print("\n")
        self._show_cursor()
        
    def animate_win(self, winner_name: str):
        if not self.animation_enabled:
            return
            
        trophy = [
            "    ___________    ",
            "   '._==_==_=_.'   ",
            "   .-\\:      /-.  ",
            "  | (|:.     |) |  ",
            "   '-|:.     |-'   ",
            "     \\::.    /    ",
            "      '::. .'      ",
            "        ) (        ",
            "      _.' '._      ",
            "     '-------'     "
        ]
        
        self._hide_cursor()
        for i in range(len(trophy)):
            self._clear_screen()
            for j in range(i + 1):
                print(Fore.YELLOW + trophy[j] + Style.RESET_ALL)
            time.sleep(self.animation_speed)
            
        print(f"\n{Fore.GREEN}🎉 {winner_name} a gagné ! 🎉{Style.RESET_ALL}")
        self._show_cursor()
        
    def animate_draw_cards(self, count: int):
        if not self.animation_enabled:
            return
            
        self._hide_cursor()
        for i in range(count):
            sys.stdout.write("\r" + " " * 40)
            sys.stdout.write("\r")
            cards_drawn = "🂠 " * (i + 1)
            sys.stdout.write(f"Pioche de cartes: {cards_drawn}")
            sys.stdout.flush()
            time.sleep(self.animation_speed)
        print("\n")
        self._show_cursor()
        
    def animate_card_effect(self, card_type: CardType):
        if not self.animation_enabled:
            return
            
        effects = {
            CardType.SKIP: "⛔",
            CardType.REVERSE: "↔️",
            CardType.DRAW_TWO: "+2",
            CardType.WILD: "🌈",
            CardType.WILD_DRAW_FOUR: "+4"
        }
        
        effect = effects.get(card_type, "")
        if not effect:
            return
            
        self._hide_cursor()
        for _ in range(3):  # 3 pulsations
            for size in range(1, 4):
                sys.stdout.write("\r" + " " * 20)
                sys.stdout.write("\r")
                sys.stdout.write(effect * size)
                sys.stdout.flush()
                time.sleep(self.animation_speed)
        print("\n")
        self._show_cursor()
        
    def toggle_animations(self):
        self.animation_enabled = not self.animation_enabled
        status = "activées" if self.animation_enabled else "désactivées"
        print(f"\nAnimations {status}")
        return self.animation_enabled

    def display_achievement(self, achievement_name: str):
        achievement_messages = {
            'first_win': "🏆 Premier Succès - Première victoire !",
            'perfect_game': "✨ Partie Parfaite - Gagner sans piocher !",
            'comeback': "🔄 Retour Victorieux - Gagner après avoir eu 10+ cartes !",
            'special_master': "🎯 Maître des Cartes Spéciales - Utiliser 5+ cartes spéciales !"
        }
        
        message = achievement_messages.get(achievement_name)
        if message:
            print(f"\n{Fore.YELLOW}=== SUCCÈS DÉBLOQUÉ ! ==={Style.RESET_ALL}")
            print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}======================{Style.RESET_ALL}\n")
            time.sleep(2)  # Pause pour que le joueur puisse lire le message

    def display_save_list(self, saves: List[Dict[str, str]]) -> Optional[str]:
        """Affiche la liste des sauvegardes et permet à l'utilisateur d'en sélectionner une"""
        if not saves:
            self.show_message("Aucune sauvegarde disponible")
            return None

        print("\nSauvegardes disponibles :")
        print("╔════════════════════════════════╗")
        for i, save in enumerate(saves, 1):
            date = datetime.fromisoformat(save['date']).strftime("%d/%m/%Y %H:%M")
            print(f"║ {i}. {save['filename']} - {date}")
        print("╚════════════════════════════════╝")

        while True:
            try:
                choice = input("\nChoisissez une sauvegarde (0 pour annuler) : ")
                if not choice.strip():
                    return None
                    
                choice = int(choice)
                if choice == 0:
                    return None
                if 1 <= choice <= len(saves):
                    # Retourner uniquement le nom du fichier
                    return saves[choice - 1]['filename']
                    
            except ValueError:
                print("Veuillez entrer un numéro valide")
            
        return None
