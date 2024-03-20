import os 
import re 

# MARK: XML to M3U8 Conversion Engine Business Logic

class ConversionEngine:
    def __init__(self) -> None:
        self.file_path = "" 

    # MARK: Validates if File Being Loaded is XML file type 
        
    def is_xml_file(self, file_path) -> bool:
        file_name = os.path.basename(file_path) 
        pattern = r"\.xml$"
        match = re.search(pattern, file_name)
        return bool(match) 
    
    # MARK: Loads File Path to Engine 

    def load_file_path(self, file_path) -> None: 
        self.file_path = file_path
        print("File Path Loaded To Engine: " + self.file_path)


    