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
        self.root.geometry("850x550")
        self.watcher = None

        # ===== TOP FRAME (buttons) =====
        self.top_frame = ctk.CTkFrame(self.root)
        self.top_frame.pack(fill="x", padx=10, pady=(10, 5))


        self.start_btn = ctk.CTkButton(self.top_frame, text="Start Watching", command=self.toggle_watch, width=250)
        self.start_btn.pack(side="left", padx=5)

        # ===== MIDDLE FRAME (path + browse) =====
        self.middle_frame = ctk.CTkFrame(self.root)
        self.middle_frame.pack(fill="x", padx=10, pady=(5, 10))

        self.paths = []  # list to store multiple folders
        self.path_var = ctk.StringVar(value="No folders selected")
        self.path_entry = ctk.CTkEntry(
            self.middle_frame,
            textvariable=self.path_var,
            width=600,
            placeholder_text="Select folder to watch..."
        )
        self.path_entry.pack(side="left", padx=5, pady=5)

        self.browse_btn = ctk.CTkButton(self.middle_frame, text="Browse", command=self.browse)
        self.browse_btn.pack(side="left", padx=5)

        # ===== TEXT AREA (logs) =====
        self.textbox = ctk.CTkTextbox(self.root, width=800, height=400)
        self.textbox.pack(padx=10, pady=(5, 10), fill="both", expand=True)



    def browse(self):
        paths = filedialog.askdirectory(mustexist=True)
        if paths:
            # Append if not already added
            if paths not in self.paths:
                self.paths.append(paths)
            # Show all paths joined by commas
            self.path_var.set(", ".join(self.paths))

    def toggle_watch(self):
        if self.watcher and self.watcher.running:
            # Stop watching
            self.watcher.stop()
            self.watcher = None
            self.start_btn.configure(text="Start Watching")
            self.textbox.insert("end", "🛑 Stopped watching folders.\n")
            self.textbox.see("end")
        else:
            # Start watching
            if not self.paths:
                messagebox.showwarning("No Folders", "Please select at least one folder.")
                return

            self.watcher = MultiFileWatcher(self.paths, callback=self.on_event)
            self.watcher.start()
            self.start_btn.configure(text="Stop Watching")
            self.textbox.insert("end", "✅ Started watching selected folders...\n")
            self.textbox.see("end")

    def start_watch(self):
        folder = self.path_var.get().strip()
        if not folder:
            messagebox.showerror("Error", "Please select a folder first.")
            return

        if not os.path.exists(folder):
            messagebox.showerror("Error", "Selected folder no longer exists!")
            return

        self.watcher = MultiFileWatcher([folder], self.on_event)  # Adjusted to use MultiFileWatcher
        self.watcher.start()
        self.start_btn.configure(text="Stop Watching")
        messagebox.showinfo("Started", f"Now watching: {folder}")

    def stop_watch(self):
        if self.watcher:
            self.watcher.stop()
            self.start_btn.configure(text="Start Watching")
            messagebox.showinfo("Stopped", "Stopped watching folder.")

    def on_event(self, event_type, path):
        line = f"[{event_type.upper()}] {path}\n"
        self.textbox.insert("end", line)
        self.textbox.see("end")
        log_event(event_type, path)

    def run(self):
        self.root.mainloop()