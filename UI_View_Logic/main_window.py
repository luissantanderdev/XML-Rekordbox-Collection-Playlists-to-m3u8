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
        self.load_file_button.grid(row=0, column=0, pady=5)

        self.no_button = tk.Button(self.window, text="No", command=self.__exit_program)
        self.no_button.grid(row=1, column=0, pady=5)
        self.no_button.grid_forget()

        self.file_label = tk.Label(self.window, text="Load a reckordbox xml playlist collection")
        self.file_label.grid(row=2, column=0, pady=5) 

        self.window.mainloop()

    # MARK: - Init State (PRIVATE)
        
    def __reset(self) -> None: 
        self.load_file_button.config(text="Load File", command=self.load_file_button_pressed)
        self.no_button.grid_forget()
        self.file_label.config(text="Load a reckordbox xml playlist collection") 

    def __exit_program(self) -> None: 
        self.window.destroy() 

    # MARK: - Generate Playlists from XML Action 
        
    def generate_playlists_button_pressed(self) -> None: 
        self.engine.load_xml_tree()
        result = self.engine.create_dictionary_of_tracks_from_collection()

        # TODO: Write This Code 
        if result: 
            self.engine.traverse_playlist_tree()
            self.engine.generate_playlists() 
            self.load_file_button.config(text="Yes", command=self.__reset)
            self.no_button.grid(row=1, column=0, pady=5) 
            self.file_label.config(text="Would You Like to Load another xml collection?")
        else: 
            print("Collection is not a valid reckordbox playlist xml")

    # MARK: - Load XML File unto Conversion Engine Action 
        
    def load_file_button_pressed(self) -> None: 
        file_path = filedialog.askopenfilename()

        result = self.engine.is_xml_file(file_path)
        
        if result: 
            self.load_file_button.config(text="Generate Playlists", command=self.generate_playlists_button_pressed)
            self.file_label.config(text=f"Selected File: {file_path}")
            self.engine.load_file_path(file_path)
        else:
            self.file_label.config(text=f"Error: Invalid File Type Must Be .xml")
