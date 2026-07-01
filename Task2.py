import mutagen as mt
from pathlib import Path
import av
import numpy as np
import sounddevice as sd
import scipy as sc



class Metadataextractor:
    def __init__(self):
        self.path = r"C:\Users\Ved Singh\Downloads\Aled_Edwards_-_All_In_My_Mind_-_Jazz_Dream_Pop.mp3"
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
        self.pcm = None
        self.full_audio = None
        self.volume = 1.0
        self.speed = 1.0
        self.sample_rate = None


        self.audio_stream_data = None
        self.audio_stream_extraction()
        self.array_extraction()

        self.audio_streaming()



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

                pcm = frame.to_ndarray()
                transposed_array = pcm.T
                self.pcm_chunks.append(transposed_array)

                pcm_info = {"Shape":pcm.shape,"Dtype":pcm.dtype}

    def volume_set(self):
        self.full_audio = self.full_audio * self.volume
    def speed_set(self):
        self.sample_rate = self.audio_stream.sample_rate*self.speed

    def filterdesign(self):
        Bass_filter = sc.signal.butter(4,250,'low',output='sos',fs=self.sample_rate)
        Low_mid_filter = sc.signal.butter(N=4,Wn=[250,1000],btype="bandpass",output='sos',fs=self.sample_rate)
        High_mid_filter = sc.signal.butter(N=4, Wn=[1000, 4000], btype="bandpass", output='sos', fs=self.sample_rate)
        Treble_filter = sc.signal.butter(N=4, Wn=[4000, 20000], btype="bandpass", output='sos', fs=self.sample_rate)
    def equalization(self):
        pass




    def audio_streaming(self):
        self.full_audio = np.concatenate(self.pcm_chunks,axis=0)
        self.volume_set()
        self.speed_set()
        play = sd.play(self.full_audio,samplerate=self.sample_rate)
        sd.wait()


















array_extract = Mp3backend()







