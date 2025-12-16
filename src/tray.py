import sys
import os
from pystray import Icon, Menu, MenuItem as item
from PIL import Image

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class TrayIcon:
    def __init__(self, lcu_connector, toggle_console_callback=None, is_visible_callback=None):
        self.lcu_connector = lcu_connector
        self.toggle_console_callback = toggle_console_callback
        self.is_visible_callback = is_visible_callback
        self.icon = None

    def _create_menu(self):
        """Creates the menu items for the tray icon."""
        menu_items = [
            item('Status: Running', None, enabled=False),
            Menu.SEPARATOR,
            item('Pause/Resume', self.toggle_pause)
        ]
        
        if self.toggle_console_callback:
            if self.is_visible_callback:
                console_text = "Hide Console" if self.is_visible_callback() else "Show Console"
            else:
                console_text = "Show/Hide Console"
            
            menu_items.append(item(console_text, self.on_toggle_console))
            
        menu_items.append(item('Exit', self.exit_app))
        
        return Menu(*menu_items)

    def on_toggle_console(self, icon, menu_item):
        """Toggles the console window visibility."""
        if self.toggle_console_callback:
            self.toggle_console_callback()
            # Refresh the menu to update the text
            self.icon.menu = self._create_menu()

    def toggle_pause(self, icon, menu_item):
        """Toggles the paused state of the LCU connector."""
        self.lcu_connector.paused = not self.lcu_connector.paused
        # This is a simple way to show state, though pystray doesn't easily support dynamic menu item text.
        # A better UX would be to change the icon, or have separate Pause and Resume items.
        # For now, a notification is clear.
        status = "Paused" if self.lcu_connector.paused else "Resumed"
        icon.notify(f"Monitoring has been {status}.")

    def exit_app(self, icon, menu_item):
        """Stops the LCU connector and the tray icon."""
        self.lcu_connector.stop()
        icon.stop()

    def run(self):
        """Creates and runs the system tray icon."""
        icon_path = resource_path("assets/gnome-thresh.ico")
        image = Image.open(icon_path)
        self.icon = Icon(
            "TFTAutoAccept",
            icon=image,
            title="TFT Auto Accept",
            menu=self._create_menu()
        )
        self.icon.run()
