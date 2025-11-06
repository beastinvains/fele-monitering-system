import customtkinter as ctk
from tkinter import filedialog, messagebox
from watcher import MultiFileWatcher
from logger import log_event
import os
import logger

class FileWatcherApp:
    def __init__(self):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.title("File Sentinel")
        self.root.geometry("950x700")
        self.watcher = None
        self.paths = []

        # ===== MAIN CONTAINER (split layout) =====
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # ===== NAVIGATION BAR (LEFT SIDE) =====
        self.navbar = ctk.CTkFrame(self.main_frame, width=200, corner_radius=0)
        self.navbar.pack(side="left", fill="y")

        ctk.CTkLabel(self.navbar, text="📁 File Sentinel", font=("Arial", 18, "bold")).pack(pady=15)

        # Nav buttons
        self.dashboard_btn = ctk.CTkButton(self.navbar, text="🏠 HOME", width=180, command=self.show_dashboard)
        self.dashboard_btn.pack(pady=5)

        self.logs_btn = ctk.CTkButton(self.navbar, text="📜 LOGS", width=180, command=self.show_logs)
        self.logs_btn.pack(pady=5)

        self.settings_btn = ctk.CTkButton(self.navbar, text="⚙️ SETTINGS", width=180, command=self.show_settings)
        self.settings_btn.pack(pady=5)

        self.settings_btn = ctk.CTkButton(self.navbar, text="🏘️ ABOUT ME", width=180, command=self.show_about_me)
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

        # Controls: show current log file, open folder, refresh, use as watch folder
        controls_frame = ctk.CTkFrame(self.content_frame)
        controls_frame.pack(fill="x", padx=10, pady=(0, 8))

        current_log = logger.get_log_file()
        ctk.CTkLabel(controls_frame, text=f"Log file: {current_log}", anchor="w").pack(side="left", padx=6)

        def open_log_dir():
            folder = os.path.dirname(current_log)
            if os.path.isdir(folder):
                try:
                    os.startfile(folder)  # Windows-specific: open explorer at folder
                except Exception as e:
                    messagebox.showerror("Error", f"Cannot open folder:\n{e}")
            else:
                messagebox.showinfo("Not found", "Log directory does not exist.")

        def use_log_dir_as_watch():
            folder = os.path.dirname(current_log)
            if not os.path.isdir(folder):
                messagebox.showinfo("Not found", "Log directory does not exist.")
                return
            if folder not in self.paths:
                self.paths.append(folder)
            # set the path_var to the chosen folder (show most recent selection)
            if hasattr(self, "path_var"):
                self.path_var.set(folder)
            messagebox.showinfo("Watch Folder Set", f"Now watching: {folder}")

        ctk.CTkButton(controls_frame, text="Open Log Directory", command=open_log_dir).pack(side="left", padx=6)
        ctk.CTkButton(controls_frame, text="Refresh", command=self.show_logs).pack(side="left", padx=6)

        # Log viewer
        log_box = ctk.CTkTextbox(self.content_frame, width=800, height=500, wrap="word")
        log_box.pack(pady=10, fill="both", expand=True)
        try:
            with open(current_log, "r", encoding="utf-8") as f:
                log_box.insert("end", f.read())
        except FileNotFoundError:
            log_box.insert("end", "No logs found yet.")
        except Exception as e:
            log_box.insert("end", f"Error reading log file: {e}")
        log_box.configure(state="disabled")

    # ========== PAGE 3: SETTINGS ==========
    def show_settings(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="⚙️ Settings", font=("Arial", 18, "bold")).pack(pady=10)

        ctk.CTkButton(self.content_frame, text="Change Log Directory", command=self.change_log_directory).pack(pady=10)
        ctk.CTkButton(self.content_frame, text="Switch Theme", command=self.toggle_theme).pack(pady=10)

    # ========= page 4: ABOUT ME ==========
    def show_about_me(self):
     self.clear_content()
     
     # Create frames for better organization
     header_frame = ctk.CTkFrame(self.content_frame)
     header_frame.pack(fill="x", padx=20, pady=(20,10))
 
     content_frame = ctk.CTkFrame(self.content_frame)
     content_frame.pack(fill="x",expand=True, padx=20, pady=10)
     
     # Define fonts
     title_font = ctk.CTkFont(family="Tw Cen MT", size=24, weight="bold")
     body_font = ctk.CTkFont(family="Tw Cen MT", size=14)
     
     # Header
     ctk.CTkLabel(
         header_frame, 
         text="🎓 ABOUT ME", 
         font=title_font
     ).pack(pady=10)
     
     # Bio text with proper formatting
     bio_text = """
      Hi, I'm Punit Sharma!
      I'm a student of BCA (Hons.) in Cyber Security at Vivekananda Institute of Professional Studies.
      I'm passionate about ethical hacking, system defense, and digital forensics — constantly learning 
      how to make technology safer and smarter.
      My ultimate goal is to become a Chief Information Security Officer (CISO) and lead teams that protect 
      organizations from cyber threats.
      This project marks my first step into Python programming. Through it, I've started exploring how 
      software can help in real-time monitoring, security automation, and event tracking — 
      all essential skills for a cybersecurity professional.
     """
     
     # Bio content
     text_widget = ctk.CTkTextbox(
         content_frame, 
         font=body_font, 
         width=600, 
         height=200,
         wrap="word"
     )
     text_widget.pack(padx=20, pady=0, fill="both", expand=True)
     text_widget.insert("1.0", bio_text)
     ctk.CTkLabel(
         content_frame, 
         text="🧠 Project Description – File Stalker", 
         font=title_font
     ).pack(pady=1)
     text_widge = ctk.CTkTextbox(
         content_frame, 
         font=body_font, 
         width=600,  
         height=350,
         wrap="word"
     )
     exp_text="""
       File Stalker is a desktop application built with Python and CustomTkinter that helps users monitor file and folder changes in real time.
       It tracks modifications, creations, deletions, and updates across multiple directories — perfect for developers, system administrators, or anyone who wants to keep an eye on their files.

       ✨ Key Features:

       📂 Watch multiple directories simultaneously

       🔔 Real-time change notifications

       🧾 Automatic event logging

       💾 Log viewer to review past file activities

       🧰 Simple and user-friendly graphical interface

       This project helped me strengthen my understanding of Python GUI development, event handling, and file system monitoring — forming the foundation for more advanced cybersecurity tools I aim to build in the future.
      """
     text_widge.pack(padx=20, pady=0, fill="both", expand=True)
     text_widge.insert("1.0", exp_text)


     
     text_widget.configure(state="disabled")  # Make text read-only

 

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
        if not path:
            return
        # append to watch list if not already present
        if path not in self.paths:
            self.paths.append(path)
        # set path_var to the selected folder (show the most recent selection)
        if not hasattr(self, "path_var"):
            # ensure path_var exists for older views
            self.path_var = ctk.StringVar(value=path)
        else:
            self.path_var.set(path)

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

    def change_log_directory(self):
        new_dir = filedialog.askdirectory(title="Select log directory", mustexist=True)
        if not new_dir:
            return
        try:
                import logger
                logfile = logger.set_log_dir(new_dir)
                messagebox.showinfo("Log Directory Changed", f"Log directory changed to:\n{new_dir}\n\nLog file:\n{logfile}")
        except Exception as e:
                messagebox.showerror("Error", f"Failed to change log directory:\n{e}")

    def run(self):
        self.root.mainloop()
