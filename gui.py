import customtkinter as ctk
from tkinter import filedialog, messagebox
from watcher import MultiFileWatcher
from logger import log_event
from plyer import notification
import os

class FileWatcherApp:
    def __init__(self):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.title("File Stalker")
        self.root.geometry("950x550")
        self.watcher = None
        self.paths = []

        # ===== MAIN CONTAINER (split layout) =====
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # ===== NAVIGATION BAR (LEFT SIDE) =====
        self.navbar = ctk.CTkFrame(self.main_frame, width=200, corner_radius=0)
        self.navbar.pack(side="left", fill="y")

        ctk.CTkLabel(self.navbar, text="📁 File Stalker", font=("Arial", 18, "bold")).pack(pady=15)

        # Nav buttons
        self.dashboard_btn = ctk.CTkButton(self.navbar, text="🏠 Dashboard", width=180, command=self.show_dashboard)
        self.dashboard_btn.pack(pady=5)

        self.logs_btn = ctk.CTkButton(self.navbar, text="📜 Logs", width=180, command=self.show_logs)
        self.logs_btn.pack(pady=5)

        self.settings_btn = ctk.CTkButton(self.navbar, text="⚙️ Settings", width=180, command=self.show_settings)
        self.settings_btn.pack(pady=5)

        # ===== MAIN CONTENT AREA =====
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.show_dashboard()  # Default view

    # ========== PAGE 1: DASHBOARD ==========
    def show_dashboard(self):
        self.clear_content()

        top_frame = ctk.CTkFrame(self.content_frame)
        top_frame.pack(fill="x", padx=10, pady=(10, 5))

        self.start_btn = ctk.CTkButton(top_frame, text="Start Watching", command=self.toggle_watch, width=250)
        self.start_btn.pack(side="left", padx=5)

        middle_frame = ctk.CTkFrame(self.content_frame)
        middle_frame.pack(fill="x", padx=10, pady=(5, 10))

        self.path_var = ctk.StringVar(value="No folders selected")
        self.path_entry = ctk.CTkEntry(middle_frame, textvariable=self.path_var, width=600, placeholder_text="Select folder to watch...")
        self.path_entry.pack(side="left", padx=5, pady=5)

        browse_btn = ctk.CTkButton(middle_frame, text="Browse", command=self.browse)
        browse_btn.pack(side="left", padx=5)

        self.textbox = ctk.CTkTextbox(self.content_frame, width=800, height=400)
        self.textbox.pack(padx=10, pady=(5, 10), fill="both", expand=True)

    # ========== PAGE 2: LOGS ==========
    def show_logs(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="📜 View Log Files", font=("Arial", 18, "bold")).pack(pady=10)
        log_box = ctk.CTkTextbox(self.content_frame, width=800, height=400)
        log_box.pack(pady=10)
        try:
            with open("logs/fs_events.jsonl", "r") as f:
                log_box.insert("end", f.read())
        except FileNotFoundError:
            log_box.insert("end", "No logs found yet.")

    # ========== PAGE 3: SETTINGS ==========
    def show_settings(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="⚙️ Settings", font=("Arial", 18, "bold")).pack(pady=10)

        ctk.CTkButton(self.content_frame, text="Switch Theme", command=self.toggle_theme).pack(pady=10)

    # ========== COMMON FUNCTIONS ==========
    def clear_content(self):
        """Clear main content area before switching page"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("dark" if current == "Light" else "light")

    def browse(self):
        path = filedialog.askdirectory(mustexist=True)
        if path and path not in self.paths:
            self.paths.append(path)
            self.path_var.set(", ".join(self.paths))

    def toggle_watch(self):
        if self.watcher and self.watcher.running:
            self.watcher.stop()
            self.watcher = None
            self.start_btn.configure(text="Start Watching")
            self.textbox.insert("end", "🛑 Stopped watching folders.\n")
            self.textbox.see("end")
        else:
            if not self.paths:
                messagebox.showwarning("No Folders", "Please select at least one folder.")
                return
            self.watcher = MultiFileWatcher(self.paths, callback=self.on_event)
            self.watcher.start()
            self.start_btn.configure(text="Stop Watching")
            self.textbox.insert("end", "✅ Started watching selected folders...\n")
            self.textbox.see("end")

    def on_event(self, event_type, path, details=None):
        line = f"[{event_type.upper()}] {path}\n"
        if hasattr(self, "textbox"):
            self.textbox.insert("end", line)
            self.textbox.see("end")
        log_event(event_type, path, details)

    def run(self):
        self.root.mainloop()
