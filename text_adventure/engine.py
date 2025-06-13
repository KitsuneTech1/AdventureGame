import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

class GameEngine:
    def __init__(self, game_data_path="game_data.json", save_dir="save_games"):
        self.game_data_path = os.path.join(script_dir, game_data_path)
        self.save_dir = os.path.join(script_dir, save_dir)
        
        self.game_data = self._load_game_data(self.game_data_path)
        self.current_room = self.game_data["start_room"]
        self._inventory = []
        
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    def _load_game_data(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def _get_room(self, room_id):
        return self.game_data["rooms"].get(room_id)

    def _get_item(self, item_id):
        return self.game_data["items"].get(item_id)

    def look(self):
        room = self._get_room(self.current_room)
        if room:
            description = f"\n{room['name']}\n{room['description']}\n"
            if room["items"]:
                description += "You see: " + ", ".join([self._get_item(item_id)['name'] for item_id in room["items"]]) + ".\n"
            
            exits = ", ".join(room["exits"].keys())
            description += f"Exits: {exits}\n"
            
            if "puzzle" in room and not room["puzzle"]["solved"]:
                description += f"There's a puzzle here: {room['puzzle']['question']}\n"
            
            return description
        return "You are in an unknown place."

    def move(self, direction):
        room = self._get_room(self.current_room)
        if room and direction in room["exits"]:
            next_room_id = room["exits"][direction]
            next_room = self._get_room(next_room_id)
            
            if next_room.get("locked") and next_room.get("unlock_item") not in self._inventory:
                return "The way is blocked by a locked door."
            
            self.current_room = next_room_id
            return self.look()
        return "You can't go that way."

    def take(self, item_name):
        room = self._get_room(self.current_room)
        if room:
            for item_id in room["items"]:
                item = self._get_item(item_id)
                if item and item_name.lower() in item["name"].lower():
                    self._inventory.append(item_id)
                    room["items"].remove(item_id)
                    return f"You picked up {item['name']}."
            return f"There is no {item_name} here."
        return "You can't take anything here."

    def inventory(self):
        if not self._inventory:
            return "Your inventory is empty."
        
        items_in_inventory = [self._get_item(item_id)['name'] for item_id in self._inventory]
        return "Inventory: " + ", ".join(items_in_inventory) + "."

    def solve_puzzle(self, answer):
        room = self._get_room(self.current_room)
        if "puzzle" in room and not room["puzzle"]["solved"]:
            if room["puzzle"]["type"] == "riddle":
                if answer.lower() == room["puzzle"]["answer"].lower():
                    room["puzzle"]["solved"] = True
                    reward_item_id = room["puzzle"].get("reward_item")
                    if reward_item_id:
                        self._inventory.append(reward_item_id)
                        reward_item_name = self._get_item(reward_item_id)['name']
                        return f"Correct! You solved the riddle and found {reward_item_name}."
                    return "Correct! You solved the riddle."
                else:
                    return "That's not the answer."
            else:
                return "There's no riddle to solve here."
        return "There's no puzzle to solve here, or it's already solved."

    def use_item(self, item_name):
        room = self._get_room(self.current_room)
        item_id_to_use = None
        for item_in_inv_id in self._inventory:
            item_in_inv = self._get_item(item_in_inv_id)
            if item_in_inv and item_name.lower() in item_in_inv["name"].lower():
                item_id_to_use = item_in_inv_id
                break
        
        if not item_id_to_use:
            return f"You don't have {item_name} in your inventory."

        if "final_puzzle" in room and room["final_puzzle"]["type"] == "item_placement":
            if item_id_to_use == room["final_puzzle"]["item_needed"]:
                self._inventory.remove(item_id_to_use)
                return room["final_puzzle"]["win_message"]
            else:
                return "That item doesn't seem to do anything here."
        elif item_id_to_use == "mirror" and self.current_room == "chamber_of_reflections":
            # Specific logic for the mirror puzzle
            if "sunstone" not in room["items"]: # Ensure sunstone is not already there
                room["items"].append("sunstone")
                return "You use the mirror to reflect a beam of light, revealing a hidden compartment! You found the Sunstone!"
            return "You've already used the mirror here."
        
        return "You can't use that item here."

    def save_state(self, filename):
        save_path = os.path.join(self.save_dir, filename + ".json")
        state = {
            "current_room": self.current_room,
            "inventory": self._inventory,
            "room_items": {room_id: self._get_room(room_id)["items"] for room_id in self.game_data["rooms"]}
        }
        with open(save_path, "w") as f:
            json.dump(state, f)
        return f"Game saved to {filename}.json"

    def load_state(self, filename):
        load_path = os.path.join(self.save_dir, filename + ".json")
        if os.path.exists(load_path):
            with open(load_path, "r") as f:
                state = json.load(f)
            self.current_room = state["current_room"]
            self._inventory = state["inventory"]
            for room_id, items in state["room_items"].items():
                if room_id in self.game_data["rooms"]:
                    self.game_data["rooms"][room_id]["items"] = items
            return f"Game loaded from {filename}.json\n{self.look()}"
        return f"No save game found with the name {filename}."
