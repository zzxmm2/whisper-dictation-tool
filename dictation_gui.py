#!/usr/bin/env python3
"""
GUI Wrapper for Whisper Dictation Tool
This provides a proper GUI interface that works when launched from favorites
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import sys
import os

class DictationGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Whisper Dictation Tool")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Set icon if available
        try:
            self.root.iconbitmap('/usr/share/icons/hicolor/scalable/apps/audio-input-microphone.svg')
        except:
            pass
        
        self.dictation_process = None
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎤 Whisper Dictation Tool", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Status: Ready", 
                                     font=("Arial", 12))
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Instructions
        instructions = """
Instructions:
1. Click 'Start Dictation' to launch the tool
2. Press Alt+D to start recording
3. Speak clearly into your microphone
4. Press Alt+D again to stop recording
5. The transcribed text will be typed automatically
6. Press Ctrl+C in the dictation window to exit
        """
        
        instruction_text = tk.Text(main_frame, height=10, width=60, wrap=tk.WORD)
        instruction_text.insert("1.0", instructions)
        instruction_text.config(state=tk.DISABLED)
        instruction_text.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        # Start button
        self.start_button = ttk.Button(button_frame, text="Start Dictation", 
                                      command=self.start_dictation)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop button
        self.stop_button = ttk.Button(button_frame, text="Stop Dictation", 
                                     command=self.stop_dictation, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Exit button
        exit_button = ttk.Button(button_frame, text="Exit", 
                                command=self.exit_app)
        exit_button.pack(side=tk.LEFT)
        
        # Log display
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="5")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=8, width=60)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for log
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Configure main frame grid weights
        main_frame.rowconfigure(4, weight=1)
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        
    def log_message(self, message):
        """Add message to log display"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_dictation(self):
        """Start the dictation tool"""
        try:
            self.log_message("🚀 Starting dictation tool...")
            self.status_label.config(text="Status: Starting...")
            
            # Get the script directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            dictation_script = os.path.join(script_dir, "dictation.py")
            
            # Start dictation tool in a subprocess
            self.dictation_process = subprocess.Popen(
                [sys.executable, dictation_script],
                cwd=script_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.log_message("✅ Dictation tool started successfully!")
            self.log_message("📋 Use Alt+D to start/stop recording")
            self.status_label.config(text="Status: Running")
            
            # Update button states
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            # Start monitoring output in a separate thread
            self.monitor_thread = threading.Thread(target=self.monitor_output, daemon=True)
            self.monitor_thread.start()
            
        except Exception as e:
            self.log_message(f"❌ Error starting dictation tool: {e}")
            messagebox.showerror("Error", f"Failed to start dictation tool:\n{e}")
            self.status_label.config(text="Status: Error")
    
    def monitor_output(self):
        """Monitor the dictation tool output"""
        try:
            for line in iter(self.dictation_process.stdout.readline, ''):
                if line:
                    self.log_message(f"📝 {line.strip()}")
        except Exception as e:
            self.log_message(f"❌ Error monitoring output: {e}")
    
    def stop_dictation(self):
        """Stop the dictation tool"""
        if self.dictation_process:
            try:
                self.log_message("⏹️ Stopping dictation tool...")
                self.dictation_process.terminate()
                self.dictation_process.wait(timeout=5)
                self.log_message("✅ Dictation tool stopped")
            except subprocess.TimeoutExpired:
                self.log_message("⚠️ Force killing dictation tool...")
                self.dictation_process.kill()
            except Exception as e:
                self.log_message(f"❌ Error stopping dictation tool: {e}")
            
            self.dictation_process = None
            
        # Update button states
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Ready")
    
    def exit_app(self):
        """Exit the application"""
        if self.dictation_process:
            self.stop_dictation()
        
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run the GUI application"""
        self.log_message("🎤 Whisper Dictation Tool GUI started")
        self.log_message("📋 Click 'Start Dictation' to begin")
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = DictationGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Failed to start GUI:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
