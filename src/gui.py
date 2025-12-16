import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys

# Import config to access QUEUE_ID_MAP and CONFIG_FILE
# Note: In a larger app, I'd separate constants, but circular import risk is low if we import inside func or careful structure.
# Here we will pass constants in or just import config module.
import config

class SettingsApp:
    def __init__(self, root, current_config, on_save_callback):
        self.root = root
        self.root.title("queueBot Settings")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        
        self.config = current_config
        self.on_save_callback = on_save_callback
        
        # Style
        self.style = ttk.Style()
        self.style.configure("TLabel", padding=5)
        self.style.configure("TButton", padding=5)
        self.style.configure("TCheckbutton", padding=2)

        # --- Main Container ---
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Discord Section ---
        discord_frame = ttk.LabelFrame(main_frame, text="Discord Integration", padding="10")
        discord_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(discord_frame, text="Webhook URL:").pack(anchor=tk.W)
        self.webhook_var = tk.StringVar(value=self.config.get("webhook_url", ""))
        ttk.Entry(discord_frame, textvariable=self.webhook_var).pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(discord_frame, text="User ID (for pings):").pack(anchor=tk.W)
        self.userid_var = tk.StringVar(value=self.config.get("user_id", ""))
        ttk.Entry(discord_frame, textvariable=self.userid_var).pack(fill=tk.X)

        # --- Notifications Section ---
        notif_frame = ttk.LabelFrame(main_frame, text="Desktop Notifications", padding="10")
        notif_frame.pack(fill=tk.X, pady=5)
        
        self.desktop_notif_var = tk.BooleanVar(value=self.config.get("desktop_notifications", True))
        ttk.Checkbutton(notif_frame, text="Enable Windows Notifications", variable=self.desktop_notif_var).pack(anchor=tk.W)

        # --- Queues Section ---
        queue_frame = ttk.LabelFrame(main_frame, text="Allowed Queues (Auto-Accept)", padding="10")
        queue_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(queue_frame, text="Uncheck all to accept ANY queue.").pack(anchor=tk.W, pady=(0, 5))

        # Scrollable Canvas for Queues
        canvas = tk.Canvas(queue_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(queue_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate Queue Checkboxes
        self.queue_vars = {}
        allowed_ids = self.config.get("allowed_queue_ids", [])
        
        # If list is empty, it means ALL are allowed (logic in main app).
        # But for UI, checking all is clearer? Or checking none?
        # Logic in config.py says: "Leave blank to accept all".
        # So if empty, we leave all unchecked? Or check all?
        # Let's interpret "Empty List" as "All Allowed" internally, but in UI:
        # If list is empty, show ALL unchecked (visually "All" or "None").
        # Actually, "Select which game modes to auto-accept" implies whitelist.
        # If whitelist is empty -> Accept All.
        # Let's stick to: If empty, all are unchecked visually, and we add a label saying "If none selected, ALL are accepted".
        
        for q_id, q_name in config.QUEUE_ID_MAP.items():
            # Check if this ID is in the allowed list
            is_checked = q_id in allowed_ids
            var = tk.BooleanVar(value=is_checked)
            self.queue_vars[q_id] = var
            ttk.Checkbutton(self.scrollable_frame, text=q_name, variable=var).pack(anchor=tk.W, fill=tk.X)

        # --- Footer ---
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(footer_frame, text="Save Settings", command=self.save_settings).pack(side=tk.RIGHT)
        ttk.Button(footer_frame, text="Cancel", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)

    def save_settings(self):
        # Gather data
        new_config = {
            "webhook_url": self.webhook_var.get().strip(),
            "user_id": self.userid_var.get().strip(),
            "desktop_notifications": self.desktop_notif_var.get(),
            "allowed_queue_ids": []
        }
        
        selected_ids = []
        for q_id, var in self.queue_vars.items():
            if var.get():
                selected_ids.append(q_id)
        
        new_config["allowed_queue_ids"] = selected_ids
        
        # Save to file
        try:
            with open(config.CONFIG_FILE, "w") as f:
                json.dump(new_config, f, indent=4)
            
            # Notify app
            if self.on_save_callback:
                self.on_save_callback(new_config)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

def open_settings(current_config, on_save_callback=None):
    """
    Opens the settings window. Blocking call.
    """
    root = tk.Tk()
    # Center window
    window_width = 450
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    app = SettingsApp(root, current_config, on_save_callback)
    
    # Set icon if available (for the window title bar)
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        icon_path = os.path.join(base_path, "assets", "gnome-thresh.ico")
        root.iconbitmap(icon_path)
    except Exception:
        pass

    root.mainloop()
