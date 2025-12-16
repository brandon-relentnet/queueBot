import json
import os
import sys
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.prompt import Prompt

# Ensure we find config.json relative to this script, not the CWD
if getattr(sys, 'frozen', False):
    # If frozen (compiled), store config next to the executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # If running from source, store config next to the script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# --- RICH THEME SETUP ---
custom_theme = Theme({
    "info": "cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "danger": "bold red",
    "highlight": "bold magenta"
})
# Defer initialization until we are sure we have a valid output stream
console = None

def init_console():
    """Initializes the Rich console object. Must be called after AllocConsole."""
    global console
    console = Console(theme=custom_theme, force_terminal=True)

# Queue ID Translation Map
QUEUE_ID_MAP = {
    1090: "TFT Normal", 1100: "TFT Ranked", 1130: "TFT Hyper Roll",
    1160: "TFT Double Up", 420: "Ranked Solo/Duo", 440: "Ranked Flex",
    400: "Draft Pick", 430: "Blind Pick", 450: "ARAM", 1700: "Arena",
    1220: "Tocker's Trials"
}

def load_or_create_config():
    """
    Loads configuration from config.json, or prompts the user to create it
    if it doesn't exist or is invalid.
    """
    # Ensure console is initialized if it hasn't been already (fallback)
    if console is None:
        init_console()

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config
        except json.JSONDecodeError:
            console.print("[danger]Config file is corrupted. Recreating...[/]")
    
    return prompt_for_config()

def prompt_for_config():
    """
    Prompts the user for configuration settings and saves them.
    """
    # Ensure console is initialized if it hasn't been already (fallback)
    if console is None:
        init_console()
        
    try:
        console.clear()
        console.print(Panel.fit("[bold white]Auto-Accept Tool Setup[/]", style="magenta"))
        
        console.print("[info]We need your Discord Webhook URL to send notifications.[/]")
        new_webhook = Prompt.ask("[bold]Paste Webhook URL (optional, press Enter to skip)[/)", default="")
        
        new_id = ""
        if new_webhook:
            console.print("\n[info]Optional: Your Discord User ID for pings (@mention).[/]")
            new_id = Prompt.ask("[bold]Paste User ID (optional, press Enter to skip)[/]", default="")

        # --- Desktop Notifications Toggle ---
        console.print("\n[info]Enable native desktop notifications?[/]")
        desktop_notifs_enabled = Prompt.ask("[bold](Y/n)[/]", choices=["y", "n"], default="y")
        
        config = {
            "webhook_url": new_webhook.strip(),
            "user_id": new_id.strip(),
            "desktop_notifications": desktop_notifs_enabled.lower() == 'y',
            "allowed_queue_ids": []
        }

        # --- Queue Selection ---
        console.print("\n[info]Select which game modes to auto-accept.[/]")
        console.print("[dim]Leave blank to accept all game modes.[/]")
        
        # Create a reverse map for easy lookup
        reverse_queue_map = {str(i+1): k for i, k in enumerate(QUEUE_ID_MAP.keys())}
        
        for i, (queue_id, name) in enumerate(QUEUE_ID_MAP.items()):
            console.print(f"  [bold cyan][{i+1}][/] {name}")
        
        choices_str = Prompt.ask("[bold]Enter numbers separated by commas (e.g., 1, 3, 5)[/]", default="")
        
        if choices_str:
            try:
                selected_indices = [choice.strip() for choice in choices_str.split(',')]
                selected_queue_ids = [reverse_queue_map[index] for index in selected_indices if index in reverse_queue_map]
                config["allowed_queue_ids"] = selected_queue_ids
                console.print(f"\n[info]Will only accept queues for: [bold green]{', '.join([QUEUE_ID_MAP[qid] for qid in selected_queue_ids])}[/][/]")
            except (ValueError, KeyError) as e:
                console.print(f"\n[danger]Invalid selection. Defaulting to all queues.[/]")
                config["allowed_queue_ids"] = [] # Default to all

        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        
        console.print("\n[success]✅ Settings saved successfully![/]\n")
        return config

    except RuntimeError as e:
        if "lost sys.stdin" in str(e):
             console.print("[danger]Cannot prompt for configuration: no interactive terminal detected.[/]")
             console.print(f"[info]Please ensure '{CONFIG_FILE}' is valid and populated, or run in an interactive terminal.[/]")
             sys.exit(1)
        raise e
