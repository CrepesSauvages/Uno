from src.ui.console_ui import ConsoleUI

class Menu:
    def __init__(self):
        self.ui = ConsoleUI()

    def choose_difficulty(self) -> str:
        while True:
            print("\n=== UNO - Choix de la difficulté ===")
            print("1. Facile")
            print("2. Moyen")
            print("3. Difficile")
            
            choice = input("Choisissez la difficulté (1-3): ")
            
            if choice == "1":
                return "facile"
            elif choice == "2":
                return "moyen"
            elif choice == "3":
                return "difficile"
            else:
                print("Choix invalide. Veuillez réessayer.")

    def ask_load_game(self) -> bool:
        while True:
            print("\n=== UNO - Charger une partie ===")
            choice = input("Voulez-vous charger une partie sauvegardée ? (o/n): ")
            
            if choice.lower() == 'o':
                return True
            elif choice.lower() == 'n':
                return False
            else:
                print("Choix invalide. Veuillez répondre par 'o' ou 'n'.")
