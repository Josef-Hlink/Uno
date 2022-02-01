from game import Game

def main():
    """
    "Activates" Game.__call__
    When this would return True, another game is started.
    When this would return False, the script is quit.
    """
    welcomeMessage: str = """
You are about to play Uno on a terminal interface.
Do not worry, the only inputs you will need to provide are typing numbers and pressing Enter.
If you want to play with multiple people on this device, you will need to pass it around.
This is so you cannot see each others cards.
You will always see all of the information you need:
- The big card will have the value in it, and the background is composed of the starting letter of its colour
- This big card represents the card that is currently on the discard pile
- Your own cards are displayed, with option numbers below them
Here are some instructions:
- To choose a card, you will need to input the corresponding option number and hit Enter
- You can always choose to pass, and you will not have to draw an (extra) card
- If you have no valid moves, you have no choice but to draw a card
IMPORTANT:
- If you have two cards, and you wish to play one of them, you have to call Uno ~before~ playing the card
- If you call Uno without any reason, or forgot to call Uno when you should have, you will draw three cards \n
    """
    
    print(welcomeMessage)
    if (input('For the best viewing experience, please adjust your terminal window to fit the following arrows entirely. \n' +
        'The terminal needs to be 40 characters high, and 112 characters wide so your hands can stay private. \n' +
        'You can skip this step by typing \'skip\' before hitting Enter.\n>')
        != 'skip'):
        print('+' + '-' * 110 + '>')
        for _ in range(38):
            print('|')
        print('V')
    
    _ = input('\nGood luck and have fun\nPlease hit Enter to start the game:\n>')
    mainGame = Game()

    if mainGame():
        main()
    else:
        quit

if __name__ == "__main__":
    main()
