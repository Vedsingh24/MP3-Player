import mutagen as mt
from pathlib import Path

class Metadataextractor:
    def __init__(self):
        self.path = None
        self.metadata = None
        self.path_config()
        self.print_path()
        self.metadata_extractor()

    def path_config(self):
        path_input = input("Paste in your mp3 file path here:(absolute)")
        path_input = path_input.strip('"')
        self.path = path_input
        self.path = Path(self.path)

    def print_path(self):
        print(type(self.path))
    def metadata_extractor(self):
        audio = mt.File(self.path)
        self.metadata = {"Title":audio['TIT2'].text[0],
                         "Artist":audio['TPE1'].text[0],
                         "Website":audio['TPUB'].text[0]}
        print(self.metadata)





Metadataextractor()
