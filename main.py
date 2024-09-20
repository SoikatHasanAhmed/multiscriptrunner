import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import subprocess
import threading
import os
import json

class MultiScriptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Script Runner")
        self.root.geometry("800x600")

        self.scripts = []
        self.processes = []
        self.output_windows = []
        self.settings_file = "script_settings.json"

        self.create_widgets()
        self.load_settings()  # Move this call after widgets are created

    def create_widgets(self):
        # Frame for buttons
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, fill=tk.X)

        self.add_script_button = tk.Button(frame, text="Add Script", command=self.add_script)
        self.add_script_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.run_button = tk.Button(frame, text="Run Scripts", command=self.run_scripts)
        self.run_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = tk.Button(frame, text="Stop Scripts", command=self.stop_scripts)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(frame, text="Save Settings", command=self.save_settings)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame for script list and output
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def add_script(self):
        script_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if script_path:
            self.scripts.append(script_path)
            self.listbox.insert(tk.END, script_path)
            self.add_output_window(script_path)

    def add_output_window(self, script_path):
        output_window = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, height=10)
        output_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        output_window.insert(tk.END, f"Output for {os.path.basename(script_path)}\n")
        self.output_windows.append(output_window)

    def run_scripts(self):
        self.processes = []
        for i, script in enumerate(self.scripts):
            process = subprocess.Popen(["python3", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.processes.append(process)
            threading.Thread(target=self.update_output, args=(process, self.output_windows[i])).start()

    def stop_scripts(self):
        for process in self.processes:
            process.terminate()

    def update_output(self, process, output_window):
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                output_window.insert(tk.END, output)
                output_window.see(tk.END)
        process.stdout.close()

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.scripts, f)
        messagebox.showinfo("Settings Saved", "Script settings saved successfully.")

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.scripts = json.load(f)
                for script in self.scripts:
                    self.listbox.insert(tk.END, script)
                    self.add_output_window(script)

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiScriptApp(root)
    root.mainloop()
