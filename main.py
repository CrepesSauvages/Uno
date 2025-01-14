from src.ui.menu import Menu
from src.game.game_manager import GameManager
from src.game.save_manager import SaveManager

def main():
    menu = Menu()
    save_manager = SaveManager()

    saves = save_manager.list_saves()
    if saves and menu.ask_load_game():
        game = GameManager("facile") 
        save_file = menu.ui.choose_save_file(saves)
        if save_file and game.load_game(save_file):
            menu.ui.show_message("Partie chargée avec succès !")
        else:
            difficulty = menu.choose_difficulty()
            game = GameManager(difficulty)
    else:
        difficulty = menu.choose_difficulty()
        game = GameManager(difficulty)
    
    game.start_game()
    
    while not game.is_game_over():
        game.play_turn()
    
    game.end_game()

if __name__ == "__main__":
    main()
