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
        self.status_var = tk.StringVar()

        self.create_widgets()
        self.load_settings()  # Load settings after widgets are created

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

        # Footer for status
        self.footer_frame = tk.Frame(self.root)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = tk.Label(self.footer_frame, textvariable=self.status_var, font=("Arial", 10))
        self.status_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.status_indicator = tk.Canvas(self.footer_frame, width=15, height=15)
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        self.update_status_indicator("stopped")

    def add_script(self):
        script_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if script_path:
            self.scripts.append(script_path)
            self.listbox.insert(tk.END, script_path)
            self.add_output_window(script_path)

    def add_output_window(self, script_path):
        # Create a frame for the output window with a title
        script_name = os.path.basename(script_path)
        output_window = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, height=10)
        output_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Insert the title and the script name at the top
        output_window.insert(tk.END, f"Output for {script_name}:\n\n")
        self.output_windows.append(output_window)

        # Set the title of the output window as a label
        title_label = tk.Label(self.output_frame, text=f"Output for {script_name}", font=("Arial", 12, "bold"))
        title_label.pack(side=tk.TOP, pady=(5, 0))

    def run_scripts(self):
        self.processes = []
        for i, script in enumerate(self.scripts):
            process = subprocess.Popen(["python3", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.processes.append(process)
            threading.Thread(target=self.update_output, args=(process, self.output_windows[i])).start()

        self.update_status_indicator("running")
        self.status_var.set("Scripts are running...")

    def stop_scripts(self):
        for process in self.processes:
            process.terminate()

        self.update_status_indicator("stopped")
        self.status_var.set("Scripts have been stopped.")

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
        self.status_var.set("Settings saved.")
        self.update_status_indicator("saved")
        messagebox.showinfo("Settings Saved", "Script settings saved successfully.")

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.scripts = json.load(f)
                for script in self.scripts:
                    self.listbox.insert(tk.END, script)
                    self.add_output_window(script)

    def update_status_indicator(self, status):
        self.status_indicator.delete("all")
        if status == "running":
            self.status_indicator.create_oval(3, 3, 12, 12, fill="green")
        elif status == "stopped":
            self.status_indicator.create_oval(3, 3, 12, 12, fill="red")
        elif status == "saved":
            self.status_indicator.create_oval(3, 3, 12, 12, fill="orange")


if __name__ == "__main__":
    root = tk.Tk()
    app = MultiScriptApp(root)
    root.mainloop()
