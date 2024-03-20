import tkinter as tk
from tkinter import filedialog

from Business_Logic.conversion_engine import ConversionEngine

# MARK: View Logic 
        
class MainWindow:
    def __init__(self):
        self.engine = ConversionEngine()

        self.window = tk.Tk()
        self.window.title("XML to M3U8 Tool")

        self.load_file_button = tk.Button(self.window, text="Load File", command=self.load_file_button_pressed)
        self.load_file_button.pack(pady=10)

        self.file_label = tk.Label(self.window, text="")
        self.file_label.pack()

        self.window.mainloop()

    def load_file_button_pressed(self) -> None: 
        file_path = filedialog.askopenfilename()

        result = self.engine.is_xml_file(file_path)

        if result: 
            self.load_file_button.destroy()
            self.convert_button = tk.Button(self.window, text="Get Playlists..")
            self.convert_button.pack()
            self.file_label.config(text=f"Selected File: {file_path}")

            self.engine.load_file_path(file_path)
        else:
            self.file_label.config(text=f"Error: Invalid File Type Must Be .xml")
