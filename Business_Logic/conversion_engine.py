import os 
import re 
import xml.etree.ElementTree as ET 
import urllib.parse

# MARK: XML to M3U8 Conversion Engine Business Logic
    # TODO: - Temporary Location of Data Objects
    # MARK: - 
    
class FolderNode:
    def __init__(self, folder_name=""):
        self.folder_name = folder_name
        self.children = []

class PlaylistNode(FolderNode):
    def __init__(self, playlist_name=""):
        super().__init__(playlist_name)
        self.track_ids = []

# =======================================================================

class ConversionEngine:
    def __init__(self) -> None:
        self.file_path = "" 

        # Constants 
        self.MUSIC_COLLECTION_ELEMENTS = {}
        self.CURRENT_WORKING_DIRECTORY = os.getcwd() 
        self.RECKORDBOX_PLAYLIST_DIRECTORY_NAME = "reckordbox_playlists"
        

    # MARK: Validates if File Being Loaded is XML file type 
        
    def is_xml_file(self, file_path) -> bool:
        file_name = os.path.basename(file_path) 
        pattern = r"\.xml$"
        match = re.search(pattern, file_name)
        return bool(match) 
    
    # MARK: Loads File Path to Engine 

    def load_file_path(self, file_path) -> None: 
        self.file_path = file_path

    # MARK: - Create Dictionary of Tracks From Collection   
    def create_dictionary_of_tracks_from_collection(self) -> bool: 
        self.collection = self.root.find('COLLECTION')

        if self.collection is None: 
            return False
        
        for tracks in self.collection:
            track_id = tracks.attrib["TrackID"]

            self.MUSIC_COLLECTION_ELEMENTS[track_id] = {
                "total_time": tracks.attrib['TotalTime'],
                "artist_name": tracks.attrib['Artist'],
                "track_name": tracks.attrib["Name"],
                "file_path": tracks.attrib["Location"]
            }

        return True
    
    # MARK: - Traverse Playlists (PRIVATE) 
    
    def __traverse_playlist(self, playlist):
        tracks = []
        for track_elements in playlist:
            track_id = track_elements.attrib['Key']
            tracks.append(track_id)
        return tracks
    
    # MARK: - Traverse Playlist Tree

    def traverse_playlists_tree_structure(self, element, depth=0): 
        # print(depth, '  ' * depth + element.tag, element.attrib, 'Type' in element.attrib)
        
        folder = FolderNode(element.attrib["Name"])

        if element.attrib["Type"] == '0':
            for child_element in element: 
                child_node = self.traverse_playlists_tree_structure(child_element, depth+1)
                folder.children.append(child_node)
        elif element.attrib["Type"] == '1':
            print("Playlist Hit")
            folder = PlaylistNode(element.attrib["Name"])
            tracks = self.__traverse_playlist(element)
            folder.track_ids.extend(tracks)

        return folder

    def traverse_playlist_tree(self): 
        self.root_folder = self.traverse_playlists_tree_structure(self.root.find("PLAYLISTS")[0])

    # MARK: - Create Rekordbox Processed Directory If None Exists
    
    def __create_reckordbox_processed_directory(self): 
        new_directory_path = os.path.join(self.CURRENT_WORKING_DIRECTORY, self.RECKORDBOX_PLAYLIST_DIRECTORY_NAME)

        if not os.path.exists(new_directory_path):
            os.makedirs(new_directory_path)

    # MARK: - Tranform Object to M3U8 String (PRIVATE)
    def __transform_object_to_m3u8(self, track) -> str: 
        total_time = track['total_time']
        artist_name = track['artist_name']
        track_name = track['track_name']
        file_path = track['file_path']

        file_path = urllib.parse.unquote(urllib.parse.urlparse(file_path).path)
        encoded_extension = f"#EXTINF:{total_time},{artist_name} - {track_name}"
        m3u8_string = f"{encoded_extension}\n{file_path}\n"

        return m3u8_string


    # MARK: Track Info M3U8 Encoder (PRIVATE)
            
    def __get_track_info_encoded_into_m3u8_string(self, playlist_track_keys) -> str:
        encoded_string = "#EXTM3U\n"

        for key in playlist_track_keys:
            track = self.MUSIC_COLLECTION_ELEMENTS[key]
            m3u8_string = self.__transform_object_to_m3u8(track)
            encoded_string += m3u8_string

        return encoded_string
    
    # MARK: - Create Playlist File 
    
    def __create_playlist_file(self, playlist_name: str, encoded_string: str, folder_path: str) -> None:
        file_path = os.path.join(folder_path, f"{playlist_name}.m3u8")

        with open(file_path, 'w') as f:
            f.write(encoded_string)
            f.close() 

    # MARK: - Create Folder Directory 
    
    def __create_directory_if_possible(self, directory_path: str) -> None:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    
    # MARK: - Travese Folder Nodes and Populate Folders with m3u8 file data 
            
    def __traverse_folder_nodes(self, root_folder, directory_path, depth=0): 
        if isinstance(root_folder, PlaylistNode):
            directory_path = directory_path[:-len(root_folder.folder_name)-1]
            encoded_string = self.__get_track_info_encoded_into_m3u8_string(root_folder.track_ids)

            self.__create_playlist_file(root_folder.folder_name, encoded_string, directory_path)
        else: 
            current_directory = os.path.join(self.RECKORDBOX_PLAYLIST_DIRECTORY_NAME, directory_path)
            self.__create_directory_if_possible(current_directory) 

            for child_folder in root_folder.children:
                next_directory = os.path.join(current_directory, child_folder.folder_name)
                self.__traverse_folder_nodes(child_folder, next_directory, depth+1)
        
        return root_folder

    # MARK: - Generate Playlists 
    def generate_playlists(self) -> None: 
        self.__create_reckordbox_processed_directory() 
        parent_directory = os.path.join(self.CURRENT_WORKING_DIRECTORY, self.RECKORDBOX_PLAYLIST_DIRECTORY_NAME)
        self.__traverse_folder_nodes(self.root_folder, parent_directory)

    # MARK: - Parses XML into a Tree. 
        
    def load_xml_tree(self) -> None: 
        self.tree = ET.parse(self.file_path)
        self.root = self.tree.getroot()
