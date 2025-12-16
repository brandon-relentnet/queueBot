# TFT Auto Accept

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

A lightweight, automated tool for **League of Legends** and **Teamfight Tactics** that instantly accepts queue ready checks. It runs silently in the system tray and integrates with Discord for remote notifications.

## 🚀 Features

*   **Auto-Accept Queues:** Instantly accepts the "Ready Check" popup.
*   **System Tray Integration:** Runs silently in the background; minimize to tray to keep your taskbar clean.
*   **Discord Notifications:** Get a ping on your phone (via Discord Webhook) when your queue pops!
*   **Game Mode Detection:** Smartly identifies if it's Ranked, ARAM, or TFT.
*   **Queue Filtering:** Configure exactly which game modes to accept (e.g., only "TFT Ranked").
*   **Zero-Interference:** Uses the LCU API directly—no screen scraping or mouse hijacking.

## 📥 Installation

### Option 1: Portable Executable (Recommended)
1.  Go to the [Releases](../../releases) page.
2.  Download the latest `TFTAutoAccept.zip`.
3.  Extract the folder anywhere on your PC.
4.  Run `TFTAutoAccept.exe`.

### Option 2: Run from Source
If you are a developer, you can run it directly with Python.

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    python main.py
    ```

## ⚙️ Configuration

On the first run, a setup wizard will appear in a console window.

1.  **Discord Webhook (Optional):** Paste a webhook URL to receive notifications.
2.  **Discord User ID (Optional):** Enter your ID (e.g., `123456789`) to get `@mentioned` when the queue pops.
3.  **Allowed Queues:** Select which modes to auto-accept (or leave blank for all).

### Modifying Settings
*   **Right-click** the system tray icon and select **Exit** to close the app.
*   Run the app with the `--update` flag to restart the wizard:
    ```bash
    TFTAutoAccept.exe --update
    ```
    *(Or simply delete the `config.json` file and restart the app)*.

## 🖥️ Usage

1.  Launch `TFTAutoAccept.exe`.
2.  The application will minimize to the system tray (look for the Thresh icon).
3.  **Right-click** the tray icon to:
    *   **Pause/Resume:** Temporarily stop auto-accepting.
    *   **Show/Hide Console:** View the activity log and debug info.
    *   **Exit:** Close the application.

## 🛠️ Building

To build the executable yourself using PyInstaller:

```bash
pip install pyinstaller
pyinstaller TFTAutoAccept.spec
```

The output will be in the `dist/` folder.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Note: This project is not endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends.*
