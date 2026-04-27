import random       

ROOMS = {
    "Blue": {
        "description": "the Blue room",
        "exits": {"south": "Yellow", "east": "White"},
    },
    "White": {
        "description": "the White room",
        "exits": {"west": "Blue"},
    },
    "Yellow": {
        "description": "the Yellow room",
        "exits": {"north": "Blue", "south": "Red"},
    },
    "Red": {
        "description": "the Red room",
        "exits": {"north": "Yellow", "west": "Green"},
    },
    "Green": {
        "description": "the Green room",
        "exits": {"east": "Red"},
        "has_exit": True,
    },
}


RIDDLES = [
    ("What has to be broken before you can use it?", ["egg", "an egg"]),
    ("I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", ["echo", "an echo"]),
    ("The more you take, the more you leave behind. What am I?", ["footsteps", "footstep", "steps"]),
    ("What comes once in a minute, twice in a moment, but never in a thousand years?", ["m", "the letter m"]),
    ("I have cities, but no houses live there. I have mountains, but no trees grow there. I have water, but no fish swim there. What am I?", ["map", "a map"]),
]


def build_exit_description(room_name, exit_locked):
    """Return the EXIT line for the Green room."""
    status = "locked" if exit_locked else "unlocked"
    return f"the EXIT to the South (EXIT is {status})"


def describe_room(room_name, boxes, dragon_room, exit_locked, has_key):
    """Print a full room description."""
    room = ROOMS[room_name]
    exits = room["exits"]
    is_exit_room = room.get("has_exit", False)

    # Build exits string
    exit_parts = []
    for direction, target in exits.items():
        exit_parts.append(f"a door {direction.capitalize()}")
    if is_exit_room:
        exit_parts.append(build_exit_description(room_name, exit_locked))

    exits_str = " and ".join(exit_parts)
    print(f"\nYou are in {room['description']}. There is {exits_str}.", end="")


    # Box in this room
    for box_color, box_room in boxes.items():
        if box_room == room_name:
            print(f" There is a {box_color} box.", end="")

    # Dragon here?
    if dragon_room == room_name:
        print(" There is a dragon here.", end="")

    # Key in inventory reminder (subtle)
    if has_key:
        print(" You are carrying the EXIT key.", end="")

    print()  # newline



def play():
    print("=" * 55)
    print(" Welcome to ZORK!")
    print(" Rooms: Green, Yellow, Red, Blue, and White.")
    print(" Find the key and escape through the EXIT.")
    print("=" * 55)


    # --- Randomise starting state -----------------
    room_names = list(ROOMS.keys())

    # Place boxes in two different rooms
    box_rooms = random.sample(room_names, 2)
    boxes = {"Gold": box_rooms[0], "Silver": box_rooms[1]}

    # One box has the key
    key_box = random.choice(["Gold", "Silver"])

    # Dragon in a random room
    dragon_room = random.choice(room_names)

    # Player starts in Yellow
    current_room = "Yellow"

    # State flags
    exit_locked = True
    has_key = False
    riddle_answered = False  # True once player got it right
    riddle_failed = False    # True if player answered wrong
    riddle_active = False    # True while waiting for answer 
    current_riddle = None

    opened_boxes = set()     # boxes the player has opened

    describe_room(current_room, boxes, dragon_room, exit_locked, has_key)

    # --- Main game loop -----------------
    while True:
        try:
            raw = input("\nUSER: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGame interrupted. Goodbye!")
            break

        if not raw:
            continue

        cmd = raw.lower()

        # --- Riddle answer mode ---------
        if riddle_active:
            _, accepted_answers = current_riddle
            if cmd in accepted_answers:
                print(f'Dragon says "correct", the key is in the {key_box} box.')
                riddle_answered = True
            else:
                print('Dragon says "wrong". He turns away and won\'t speak to you again.')
                riddle_failed = True
            riddle_active = False
            continue

        # --- Movement -------------------
        if cmd.startswith("go "):
            direction = cmd[3:].strip()
            room = ROOMS[current_room]
            exits = room["exits"]

            # Special: "go exit" or "go south" in Green when unlocked
            if room.get("has_exit") and direction == "south":
                if not exit_locked:
                    print("\nCongratulations! You made it!")
                    break
                else:
                    print("The EXIT is locked. You need the key first.")
                    continue

            if direction in exits:
                current_room = exits[direction]
                describe_room(current_room, boxes, dragon_room, exit_locked, has_key)
            else:
                print(f"There is no door to the {direction} here.")


        # --- Exit the building ------------
        elif cmd == "exit":
            if current_room == "Green" and not exit_locked:
                print("\nCongratulations! You made it!")
                break
            elif current_room == "Green" and exit_locked:
                print("The EXIT is locked. You need to unlock it first.")
            else:
                print("There is no EXIT here.")


        # --- Unlock exit ------------------
        elif cmd == "unlock exit":
            if current_room != "Green":
                print("There is no EXIT here to unlock.")
            elif not has_key:
                print("You don't have the key, EXIT is still locked.")
            elif not exit_locked:
                print("The EXIT is already unlocked.")
            else:
                exit_locked = False
                print("The EXIT is unlocked now.")


        # --- Open box ---------------------
        elif cmd == "open box" or cmd.startswith("open "):
            # Find which box(es) are in this room
            boxes_here = [color for color, room in boxes.items() if room == current_room]
            if not boxes_here:
                print("There is no box here.")
            else:
                box_color = boxes_here[0]   # open the one that's there
                if box_color in opened_boxes:
                    print(f"The {box_color} box is already open.")
                else:
                    opened_boxes.add(box_color)
                    print(f"The {box_color} box is open.")
                    # Wrong box -> lock the other permanently, player loses
                    if box_color != key_box:
                        other = "Gold" if box_color == "Silver" else "Silver"
                        print(f"The {other} box snaps shut with a loud CLICK and locks permanently.")
                        print("You opened the wrong box. You LOSE. Better luck next time!")
                        break


        # --- Get key -----------------------
        elif cmd == "get key":
            boxes_here = [color for color, room in boxes.items() if room == current_room]
            if not boxes_here:
                print("There is no box here.")
            else:
                box_color = boxes_here[0]
                if box_color not in opened_boxes:
                    print(f"The {box_color} box is not open yet.")
                elif box_color != key_box:
                    print("There is no key in this box.")
                elif has_key:
                    print("You already have the key.")
                else:
                    has_key = True
                    print("You have the EXIT key now.")


        # --- Dragon interaction ----------------
        elif cmd == "where is the key":
            if dragon_room != current_room:
                print("There is no dragon here.")
            elif riddle_answered:
                print(f'Dragon reminds you: the key is in the {key_box} box.')
            elif riddle_failed:
                print("The dragon ignores you.")
            else:
                print("Dragon says you need to answer a question to tell you where the key is.")

        
        elif cmd == "ask me":
            if dragon_room != current_room:
                print("There is no dragon here.")
            elif riddle_answered:
                print("The dragon has already told you what you need to know.")
            elif riddle_failed:
                print("The dragon ignores you.")
            else:
                current_riddle = random.choice(RIDDLES)
                question, _ = current_riddle
                print(f'Dragon asks "{question}"')
                riddle_active = True

        
        # --- Look / inventory ------------
        elif cmd in ("look", "l"):
            describe_room(current_room, boxes, dragon_room, exit_locked, has_key)

        elif cmd in ("inventory", "i", "inv"):
            if has_key:
                print("You are carrying: EXIT key.")
            else:
                print("You are carrying nothing.")

        elif cmd in ("help", "?"):
            print("""
Commands:
    go [north/south/east/west]  - move between rooms
    look                        - describe current room
    open box                    - open the box in this room
    get key                     - pick up the key from an open box
    where is the key            - ask the dragon (must be in the same room)
    ask me                      - get the dragon's riddle
    unlock exit                 - use the key to unlock the EXIT
    exit                        - escape through the unlocked EXIT
    inventory                   - check what you're carrying
    help                        - show list
""")
            
        else:
            print("I don't understand that. Type 'help' for a list of commands.")


if __name__ == "__main__":
    play()