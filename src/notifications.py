import sys
import os
import aiohttp
from plyer import notification
import config


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def send_desktop_notification(game_mode):
    """
    Sends a native desktop notification.
    """
    try:
        icon_path = resource_path("gnome-thresh.ico")
        notification.notify(
            title="Queue Popped!",
            message=f"Accepting match for {game_mode}.",
            app_name="TFT Auto Accept",
            app_icon=icon_path,
            timeout=10  # Notification will disappear after 10 seconds
        )
        config.console.log("[cyan]Desktop notification sent.[/]")
    except Exception as e:
        config.console.log(f"[yellow]Failed to send desktop notification: {e}[/]")


async def send_discord_ping(webhook_url, user_id, game_mode):
    """
    Sends a notification to the configured Discord webhook.
    """
    if not webhook_url:
        return
        
    mention = f"<@{user_id}>" if user_id else ""
    
    async with aiohttp.ClientSession() as session:
        try:
            payload = {
                "content": f"{mention} 🚨 **QUEUE POPPED!** 🚨\n**Mode:** {game_mode}\nAccepting match automatically."
            }
            await session.post(webhook_url, json=payload)
            config.console.log("[cyan]Discord notification sent.[/]")
        except Exception as e:
            config.console.log(f"[yellow]Failed to send Discord ping: {e}[/]")
