# Multi-Script Runner GUI Application

This application provides a graphical user interface (GUI) to manage, run, and monitor multiple Python scripts concurrently. It allows you to start, stop, and view the output of each script within the same window. Additionally, the application saves your script list so that you can easily load and run them again later.

## Features

- **Add Python Scripts**: Easily add Python scripts to the list for execution.
- **Start/Stop Scripts**: Start or stop individual scripts from the GUI.
- **View Script Output**: Monitor the output of each running script in real-time within the application.
- **Persistent Settings**: The list of scripts is saved in a `script_settings.txt` file and loaded automatically on startup.

## Requirements

- Python 3.x
- `tkinter` (usually included with Python)
- `subprocess`
- `threading`

## Installation

1. Clone the repository or download the source code files.
2. Ensure that you have Python 3 installed on your system.
3. Install the required Python libraries (if not already installed).

## Usage

1. **Running the Application:**
   - Navigate to the directory containing the `main.py` script.
   - Run the script using the following command:
     ```bash
     python3 main.py
     ```

2. **Adding Scripts:**
   - Click the "Add Script" button.
   - A file dialog will open. Navigate to the Python script you want to add and select it.
   - The script will be added to the list.

3. **Starting a Script:**
   - Select a script from the list.
   - Click the "Start Script" button to run the selected script.
   - The output of the script will be displayed in the output window on the right.

4. **Stopping a Script:**
   - Select the script that is currently running from the list.
   - Click the "Stop Script" button to terminate the script.

5. **Removing a Script:**
   - Select the script from the list.
   - Click the "Remove Script" button to remove the script from the list.
   - The settings will be saved automatically.

6. **Saving and Loading Settings:**
   - The application automatically saves the list of scripts to `script_settings.txt` when you add or remove scripts.
   - When you reopen the application, the scripts listed in `script_settings.txt` will be loaded automatically.

## Notes

- The application uses the `subprocess` module to run scripts, and each script's output is captured and displayed within the GUI.
- Scripts must be compatible with Python 3.
- The `script_settings.txt` file is saved in the same directory as the application and can be manually edited if necessary.

## Troubleshooting

- **Error when adding a script**: Ensure the selected file is a valid Python script (`.py` extension).
- **Script not stopping**: If a script does not terminate when the "Stop Script" button is clicked, you may need to manually kill the process from your operating system's task manager.

## License

This project is provided under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request.

## Contact

For any issues or questions, please open an issue on the GitHub repository or contact the maintainer directly.
