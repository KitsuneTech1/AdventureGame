from engine import GameEngine

def run_game():
    engine = GameEngine()
    print("Welcome to the Text Adventure!")
    print(engine.look())

    while True:
        command = input("> ").lower().strip()
        parts = command.split(" ", 1)
        action = parts[0]
        argument = parts[1] if len(parts) > 1 else None

        if action == "quit":
            print("Thanks for playing!")
            break
        elif action == "look":
            print(engine.look())
        elif action == "inventory":
            print(engine.inventory())
        elif action == "go":
            if argument:
                print(engine.move(argument))
            else:
                print("Go where?")
        elif action == "take":
            if argument:
                print(engine.take(argument))
            else:
                print("Take what?")
        elif action == "solve":
            if argument:
                print(engine.solve_puzzle(argument))
            else:
                print("Solve what?")
        elif action == "use":
            if argument:
                print(engine.use_item(argument))
            else:
                print("Use what?")
        elif action == "save":
            if argument:
                print(engine.save_state(argument))
            else:
                print("Save as what?")
        elif action == "load":
            if argument:
                print(engine.load_state(argument))
            else:
                print("Load what?")
        else:
            print("Invalid command. Try 'go [direction]', 'take [item]', 'look', 'inventory', 'solve [answer]', 'use [item]', 'save [filename]', 'load [filename]', or 'quit'.")

if __name__ == "__main__":
    run_game()
