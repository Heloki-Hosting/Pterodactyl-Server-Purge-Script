import time
import sys
import os
from dotenv import load_dotenv
from pydactyl import PterodactylClient
import signal

exit_requested = False 

load_dotenv()

PANEL_URL = os.getenv("PANEL_URL")
API_KEY = os.getenv("API_KEY")
os.system("clear")
api = PterodactylClient(PANEL_URL, API_KEY)
userid = 1
excluded_users = {298, 385} 

def rgb(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def type_effect(text, start_color=(255, 100, 255), delay=0.05):
    for i, char in enumerate(text):
        r = max(0, start_color[0] - i * 5)
        g = min(255, start_color[1] + i * 2)
        b = start_color[2]
        sys.stdout.write(rgb(r, g, b, char))
        sys.stdout.flush()
        time.sleep(delay)
    print()

ascii_art = r"""
 __    __          __          __       __        __    __                     __     __                   
/  |  /  |        /  |        /  |     /  |      /  |  /  |                   /  |   /  |                  
$$ |  $$ | ______ $$ | ______ $$ |   __$$/       $$ |  $$ | ______   _______ _$$ |_  $$/ _______   ______  
$$ |__$$ |/      \$$ |/      \$$ |  /  /  |      $$ |__$$ |/      \ /       / $$   | /  /       \ /      \ 
$$    $$ /$$$$$$  $$ /$$$$$$  $$ |_/$$/$$ |      $$    $$ /$$$$$$  /$$$$$$$/$$$$$$/  $$ $$$$$$$  /$$$$$$  |
$$$$$$$$ $$    $$ $$ $$ |  $$ $$   $$< $$ |      $$$$$$$$ $$ |  $$ $$      \  $$ | __$$ $$ |  $$ $$ |  $$ |
$$ |  $$ $$$$$$$$/$$ $$ \__$$ $$$$$$  \$$ |      $$ |  $$ $$ \__$$ |$$$$$$  | $$ |/  $$ $$ |  $$ $$ \__$$ |
$$ |  $$ $$       $$ $$    $$/$$ | $$  $$ |      $$ |  $$ $$    $$//     $$/  $$  $$/$$ $$ |  $$ $$    $$ |
$$/   $$/ $$$$$$$/$$/ $$$$$$/ $$/   $$/$$/       $$/   $$/ $$$$$$/ $$$$$$$/    $$$$/ $$/$$/   $$/ $$$$$$$ |
                                                                                                 /  \__$$ |
                                                                                                 $$    $$/ 
                                                                                                  $$$$$$/  
"""

for i, line in enumerate(ascii_art.split("\n")):
    color = (255 - i * 10, 100 + i * 5, 255)  
    print(rgb(*color, line))
    time.sleep(0.05)

def type_effect_smooth(text, color=(255, 100, 255), delay=0.05):
    """Smooth typing effect with a static color."""
    for char in text:
        sys.stdout.write(rgb(*color, char))
        sys.stdout.flush()
        time.sleep(delay)
    print()


def handle_exit(signum, frame):
    global exit_requested
    if exit_requested:
        print(rgb(255, 50, 50, "\n[!] Force exit detected. Exiting..."))
        exit(0)
    
    exit_requested = True
    print(rgb(255, 150, 50, "\n[?] CTRL+C detected. Press again to exit, or continue."))

signal.signal(signal.SIGINT, handle_exit)    

time.sleep(0.5)
type_effect_smooth("Discord  : @hellcat_xyz", color=(88, 101, 242))

time.sleep(0.5)
type_effect_smooth("Server   : https://discord.gg/kehSwBnEz2", color=(88, 101, 242))

time.sleep(0.5)
type_effect_smooth("Telegram : @helokihost\n", color=(0, 136, 204))


type_effect("Enter a keyword to start purging: ", start_color=(255, 100, 255))
keyword = input(rgb(255, 100, 255, "> ")) 

type_effect("Enter the maximum user ID: ", start_color=(255, 100, 255))  
max_userid = int(input(rgb(255, 100, 255, "> "))) 

type_effect(f"\n[+] Keyword '{keyword}' received. Scanning up to user ID {max_userid}...\n", start_color=(255, 100, 255))

def type_effect_gradient(text, line_index, start_color=(255, 100, 255), delay=0.05):
    """Typing effect with the same gradient used in ASCII art."""
    r = max(0, start_color[0] - line_index * 10)
    g = min(255, start_color[1] + line_index * 5)
    b = start_color[2]

    for char in text:
        sys.stdout.write(rgb(r, g, b, char))
        sys.stdout.flush()
        time.sleep(delay)
    print()

def type_effect_error(text, delay=0.05):
    """Typing effect for errors in red color."""
    r, g, b = 255, 50, 50  # Red color for errors
    for char in text:
        sys.stdout.write(rgb(r, g, b, char))
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Main loop
while userid <= max_userid:
    try:
        user = api.user.get_user_info(user_id=userid, includes=['servers'])

        for i, server in enumerate(user["attributes"].get("relationships", {}).get("servers", {}).get("data", [])):
            server_name = server["attributes"]["name"].lower()
            
            type_effect_gradient(f"Checking {server_name}", i)

            if keyword.lower() in server_name:
                type_effect_gradient(f"Skipping {server_name} (contains '{keyword}')", i)
                continue

            if userid in excluded_users:
                type_effect_gradient(f"Skipping {server_name} (User ID: {userid})", i)
                continue

            type_effect_gradient(f"Deleting {server['attributes']['name']}", i)
            api.servers.delete_server(server["attributes"]["id"])

    except Exception as e:
        error_message = f"\n[!] Error processing user {userid}: {str(e)}\n"
        type_effect_error(error_message)

    userid += 1
    time.sleep(0.1)