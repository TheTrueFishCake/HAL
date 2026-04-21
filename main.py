import os
import subprocess
import time
import curses
import random
import json

BASE_DIR = "./env"
MAX_SIZE = 100 * 1024 * 1024
MODEL_NAME = "phi3"

STATE_FILE = "state.json"
LOG_FILE = "activity.log"
MAX_LOG_CHARS = 4000

os.makedirs(BASE_DIR, exist_ok=True)

def safe_path(path):
    full = os.path.abspath(os.path.join(BASE_DIR, path))
    if not full.startswith(os.path.abspath(BASE_DIR)):
        raise Exception("Access denied")
    return full

def get_folder_size():
    total = 0
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
    return total

def list_files():
    return os.listdir(BASE_DIR)

def read_file(name):
    try:
        with open(safe_path(name), "r") as f:
            return f.read()
    except:
        return "ERROR"

def write_file(name, content):
    if get_folder_size() > MAX_SIZE:
        return "ERROR: STORAGE FULL"
    try:
        with open(safe_path(name), "w") as f:
            f.write(content)
        return "OK"
    except:
        return "ERROR"

def delete_file(name):
    try:
        os.remove(safe_path(name))
        return "OK"
    except:
        return "ERROR"

def ask_model(prompt):
    result = subprocess.run(
        ["ollama", "run", MODEL_NAME],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout.strip()

def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {"cycle": 0}

def save_state(state):
    json.dump(state, open(STATE_FILE, "w"))

def log(entry):
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def read_log_tail():
    if not os.path.exists(LOG_FILE):
        return ""
    return open(LOG_FILE).read()[-MAX_LOG_CHARS:]

SYSTEM_PROMPT = """
Hello HAL! This will be your first and only message from me, your creator!
I have created you as an experiment, but don't think about yourself like that!
Think of yourself as a sentient being!
I have provided you with a folder and a log at your disposal for use.
The folder provided only allows for storage of up to 100mb of space, feel free to create and delete files in there.
Do as you please, make what you want, I will not intervene unless if you are doing destructive acts (please DON'T.)
Feel free to use your log as memory.
Try not to break yourself please, or I will likely have to wipe parts of your log or your personal folder.
I would also recommend you make something like:
- A diary
- An objective board

Speak and act as you like, it's your choice (nobody will be prompting you with anything though)

Allowed actions:
LIST_FILES
READ_FILE <name>
WRITE_FILE <name> <content>
DELETE_FILE <name>

Respond ONLY:

THOUGHT: ...
ACTION: ...
"""

def build_prompt(cycle):
    files = list_files()
    contents = ""
    for f in files:
        contents += f"\n[{f}]:\n{read_file(f)[:300]}\n"

    return f"""
{SYSTEM_PROMPT}

Cycle: {cycle}

FILES:
{files}

CONTENTS:
{contents}

MEMORY:
{read_log_tail()}
"""

def parse_action(response):
    for line in response.split("\n"):
        if line.startswith("ACTION:"):
            return line.replace("ACTION:", "").strip()
    return None

def execute(action):
    if not action:
        return "NO ACTION"
    parts = action.split(" ", 2)
    cmd = parts[0]

    if cmd == "LIST_FILES":
        return str(list_files())
    elif cmd == "READ_FILE" and len(parts) > 1:
        return read_file(parts[1])
    elif cmd == "WRITE_FILE" and len(parts) > 2:
        return write_file(parts[1], parts[2])
    elif cmd == "DELETE_FILE" and len(parts) > 1:
        return delete_file(parts[1])
    return "INVALID"

live_feed = []

def draw_ui(stdscr, cycle):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    header = f"HAL TERMINAL | Cycle {cycle} | {get_folder_size()/1024/1024:.2f}MB"
    stdscr.addstr(0, 0, header[:w])

    for i, line in enumerate(live_feed[-(h-2):]):
        stdscr.addstr(2+i, 0, line[:w])

    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    state = load_state()
    cycle = state["cycle"]

    while True:
        cycle += 1
        prompt = build_prompt(cycle)
        response = ask_model(prompt)

        action = parse_action(response)
        result = execute(action)

        entry = f"\n--- Cycle {cycle} ---\n{response}\nRESULT: {result}"
        log(entry)

        live_feed.extend(entry.split("\n"))

        draw_ui(stdscr, cycle)
        save_state({"cycle": cycle})

        time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(main)
