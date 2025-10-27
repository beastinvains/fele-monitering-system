import customtkinter as ctk
from tkinter import filedialog, messagebox
from watcher import FileWatcher
from logger import log_event
import os

class FileWatcherApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("File Watch Pro")
        self.root.geometry("850x550")

        self.watcher = None

        # Top bar
        self.path_var = ctk.StringVar()
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="x", padx=10, pady=10)

        self.path_entry = ctk.CTkEntry(self.frame, textvariable=self.path_var, width=500, placeholder_text="Select folder to watch...")
        self.path_entry.pack(side="left", padx=5)

        self.browse_btn = ctk.CTkButton(self.frame, text="Browse", command=self.browse)
        self.browse_btn.pack(side="left", padx=5)

        self.start_btn = ctk.CTkButton(self.frame, text="Start Watching", command=self.toggle_watch)
        self.start_btn.pack(side="left", padx=5)

        # Table
        self.textbox = ctk.CTkTextbox(self.root, width=800, height=400)
        self.textbox.pack(padx=10, pady=10, fill="both", expand=True)

    def browse(self):
        folder = filedialog.askdirectory()
        if folder:
            if os.path.exists(folder):
                self.path_var.set(folder)
            else:
                messagebox.showerror("Error", "Selected folder does not exist!")
                self.path_var.set("")
        else:
            self.path_var.set("")

    def toggle_watch(self):
        if self.watcher and self.watcher.running:
            self.stop_watch()
        else:
            self.start_watch()

    def start_watch(self):
        folder = self.path_var.get().strip()
        if not folder:
            messagebox.showerror("Error", "Please select a folder first.")
            return
    
        if not os.path.exists(folder):
            messagebox.showerror("Error", "Selected folder no longer exists!")
            return
        
        self.watcher = FileWatcher(folder, self.on_event)
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