import mutagen as mt
from pathlib import Path
import av
import numpy as np
import sounddevice as sd
import scipy as sc
from scipy import signal



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
        self.pcm = None
        self.full_audio = None
        self.volume = 1.0
        self.speed = 1.0
        self.sample_rate = None
        self.bass_audio = None
        self.low_mid_audio = None
        self.high_mid_audio = None
        self.treble_audio = None
        self.bass_vol = 1.2
        self.lowmid_vol = 1.1
        self.highmid_vol = 0.9
        self.treble_vol = 0.2



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
        self.bass_filter = signal.butter(4,250,'low',output='sos',fs=self.sample_rate)
        self.low_mid_filter = signal.butter(N=4,Wn=[250,1000],btype="bandpass",output='sos',fs=self.sample_rate)
        self.high_mid_filter = signal.butter(N=4, Wn=[1000, 4000], btype="bandpass", output='sos', fs=self.sample_rate)
        self.treble_filter = signal.butter(N=4, Wn=[4000, 20000], btype="bandpass", output='sos', fs=self.sample_rate)
    def equalization(self):
        self.filterdesign()
        self.bass_audio = signal.sosfiltfilt(self.bass_filter,self.full_audio)*self.bass_vol
        self.low_mid_audio = signal.sosfiltfilt(self.low_mid_filter,self.full_audio)*self.lowmid_vol
        self.high_mid_audio = signal.sosfiltfilt(self.high_mid_filter,self.full_audio)*self.highmid_vol
        self.treble_audio = signal.sosfiltfilt(self.treble_filter,self.full_audio)*self.treble_vol
        self.full_audio = self.bass_audio + self.low_mid_audio + self.high_mid_audio + self.treble_audio






    def audio_streaming(self):
        self.full_audio = np.concatenate(self.pcm_chunks,axis=0)

        self.volume_set()
        self.speed_set()
        play = sd.play(self.full_audio,samplerate=self.sample_rate)
        sd.wait()


















array_extract = Mp3backend()







