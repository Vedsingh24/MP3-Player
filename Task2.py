import mutagen as mt
from pathlib import Path
import av
import numpy

class Metadataextractor:
    def __init__(self):
        self.path = r"C:\Users\Ved Singh\Downloads\Alone_-_Color_Out.mp3"
        self.metadata = None
        # self.path_config()
        # self.metadata_extractor()


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

metadata = Metadataextractor()

class Mp3backend:
    def __init__(self):
        self.path= metadata.path
        self.metadeta = metadata.metadata
        self.decoded_sample = None
        self.audio_stream = None
        self.pcm_chunks = []


        self.audio_stream_data = None
        self.audio_stream_extraction()
        self.array_extraction()


    def audio_stream_extraction(self):
        self.decoded_sample=av.open(self.path)
        for streams in self.decoded_sample.streams:
            print(streams)
            self.audio_stream= self.decoded_sample.streams.audio[0]
            self.audio_stream_data = {"codec context":self.audio_stream.codec_context,"sample rate":self.audio_stream.sample_rate,"channels":self.audio_stream.channels}
            print(self.audio_stream_data)

    def array_extraction(self):
        print(type(self.decoded_sample))
        for packets in self.decoded_sample.demux(self.audio_stream):
            for frame in packets.decode():
                frame_info = {"Format":frame.format,"Layout":frame.layout, "Sample rate":frame.sample_rate}
                print(frame_info)
                pcm = frame.to_ndarray()
                print(type(pcm))
                pcm_info = {"Shape":pcm.shape,"Dtype":pcm.dtype}
                print(pcm_info)










array_extract = Mp3backend()







