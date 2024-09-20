import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import subprocess
import threading
import os
import json

class MultiScriptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Script Runner")
        self.root.geometry("800x600")  # Set initial size

        self.scripts = []
        self.processes = []
        self.output_windows = []
        self.settings_file = "script_settings.json"

        self.create_widgets()
        self.load_settings()

        # Add a key binding to toggle full screen
        self.root.bind("<F11>", self.toggle_fullscreen)  # Use F11 to toggle full screen

    def create_widgets(self):
        # Frame for buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.add_script_button = ttk.Button(button_frame, text="Add Script", command=self.add_script)
        self.add_script_button.pack(side=tk.LEFT, padx=5)

        self.run_button = ttk.Button(button_frame, text="Run Scripts", command=self.run_scripts)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop Scripts", command=self.stop_scripts)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.remove_script_button = ttk.Button(button_frame, text="Remove Script", command=self.remove_script)
        self.remove_script_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(button_frame, text="Save Settings", command=self.save_settings)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Frame for script list
        self.script_frame = ttk.Frame(self.root)
        self.script_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.listbox = tk.Listbox(self.script_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Frame for output
        self.output_frame = ttk.Frame(self.root)
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.status_bar = ttk.Label(self.root, text="Status: Ready", relief=tk.SUNKEN, anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def toggle_fullscreen(self, event=None):
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)

    def add_script(self):
        script_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if script_path:
            self.scripts.append(script_path)
            self.listbox.insert(tk.END, script_path)
            self.add_output_window(script_path)

    def add_output_window(self, script_path):
        output_frame = ttk.Frame(self.output_frame)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        label = ttk.Label(output_frame, text=os.path.basename(script_path))
        label.pack(anchor='nw')

        output_window = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10)
        output_window.pack(fill=tk.BOTH, expand=True)
        output_window.insert(tk.END, f"Output for {os.path.basename(script_path)}:\n")
        self.output_windows.append(output_window)

    def run_scripts(self):
        self.processes = []
        running_scripts = []
        for i, script in enumerate(self.scripts):
            process = subprocess.Popen(["python3", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.processes.append(process)
            running_scripts.append(os.path.basename(script))
            threading.Thread(target=self.update_output, args=(process, self.output_windows[i])).start()

        self.status_bar.config(text=f"Running: {', '.join(running_scripts)}")

    def stop_scripts(self):
        for process in self.processes:
            process.terminate()
        self.status_bar.config(text="All scripts stopped.")

    def remove_script(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.scripts[index]
            self.listbox.delete(index)
            self.output_windows[index].destroy()
            del self.output_windows[index]

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
        self.status_bar.config(text="Settings saved.")

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
