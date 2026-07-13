<p align="center"><a href="https://kitsunetechnologies.org/work"><img src="https://raw.githubusercontent.com/KitsuneTech1/.github/main/assets/kitsune-banner.svg" alt="Built by Kitsune Technologies" width="760"></a></p>

# Adventure Game

A small command-line text adventure. Explore a jungle temple, pick up items, solve a riddle, and find the Sunstone.

## What it is

A Python text adventure that runs entirely in your terminal. You move between rooms, pick up and use items, and solve a riddle to unlock the final chamber. The game world (rooms, items, the riddle, the win condition) is defined in `text_adventure/game_data.json` and loaded by the game engine, so there is nothing to compile or configure, just run it.

The map is a jungle clearing leading into an ancient stone temple: a foyer branches out into a hall of echoes, an archive with a sphinx and a riddle, a garden of stone, a chamber of reflections with a mirror puzzle, and a locked altar room where you place the Sunstone to win.

You can save your progress to a named file and load it back later.

## Requirements

- Python 3 (developed and tested on Python 3.14; anything 3.8+ should work fine, no version-specific syntax is used).
- No third-party packages. The game only uses Python's standard library (`json`, `os`), so there is nothing to `pip install` and no `requirements.txt`.

## Run it

**Clone and run:**

```
git clone https://github.com/KitsuneTech1/AdventureGame.git
cd AdventureGame
python3 text_adventure/game.py
```

Run it from the repository root exactly as above. The game finds its data file (`game_data.json`) and save folder relative to `engine.py`'s own location, so it works whether you launch it from the repo root or from inside the `text_adventure` folder.

**From inside the `text_adventure` folder:**

```
cd AdventureGame/text_adventure
python3 game.py
```

**Don't have git? Download the ZIP:**

1. On the GitHub repo page, click Code, then Download ZIP.
2. Unzip it.
3. Open a terminal in the unzipped folder and run:

```
python3 text_adventure/game.py
```

## How to play

Type a command at the `>` prompt and press Enter. Commands are case-insensitive.

- `look` - reprint the description of the room you're in, what's visible, and the exits.
- `inventory` - list what you're carrying.
- `go <direction>` - move through an exit, e.g. `go east`. If the room ahead is locked, you'll need the right item in your inventory first.
- `take <item>` - pick up an item lying in the current room, e.g. `take mirror`. You can type part of the item's name.
- `use <item>` - use an item you're carrying, e.g. `use mirror`. Some rooms react to specific items (the mirror in the Chamber of Reflections, the Sunstone on the final altar).
- `solve <answer>` - answer a riddle in the current room, e.g. `solve echo`.
- `save <filename>` - save your current room, inventory, and room contents to `text_adventure/save_games/<filename>.json`.
- `load <filename>` - load a previously saved game by name.
- `quit` - exit the game.

Any other input prints a reminder of these commands (there's no separate `help` command, the parser just falls back to listing them).

### Example session

```
Welcome to the Text Adventure!

Jungle Clearing
You stand in a humid jungle clearing...
Exits: east

> go east
Temple Entrance
...
> go north
Grand Foyer
...
> go north
Hall of Echoes
...
> go east
Archive of Whispers
...
There's a puzzle here: I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?
> solve echo
Correct! You solved the riddle and found a skeletal key.
> save progress
Game saved to progress.json
```

## License

MIT. See [LICENSE.md](LICENSE.md).
