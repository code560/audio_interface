# -*- coding: utf-8 -*-
import wave
import threading
from Queue import Queue
import time
import pyaudio

import sys
import pdb

# defines
CHUNK = 1024


class SoundPlayer:

    def __init__(self):
        # flags
        self.loop = False
        
        # event flags
        self.paused = threading.Event()

        # sounds queue
        self.sounds = Queue()



    def playsound(self, wavfile):
        if (wavfile == ""):
            return

        # open file
        print('open file = {}'.format(wavfile))
        wf = wave.open(wavfile, 'rb')

        wfinfo = wf.getparams()
        print(wfinfo)
        print('wave file info')
        print('channels = {}'.format(wfinfo[0]))
        print('sampling width = {} byte'.format(wfinfo[1]))
        print('frame rate = {} Hz'.format(wfinfo[2]))
        print('frame count = {}'.format(wfinfo[3]))
        print('sound time = {} s'.format((int)(wfinfo[3] / wfinfo[2])))

        # def non-blocking callback
        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            if self.paused.is_set():
                print('paused sound.')
                return (data, pyaudio.paComplete)
            else:
                print('non-blocking play ({}, {}, {}, {})'.format(in_data, frame_count, time_info, status))
                return (data, pyaudio.paContinue)

        # open stream
        p = pyaudio.PyAudio()
        s = p.open(format=p.get_format_from_width(wf.getsampwidth()), 
                   channels=wf.getnchannels(), 
                   rate=wf.getframerate(), 
                   output=True,
                   stream_callback=callback)

        # play stream
        s.start_stream()
        print('started non-blocking sound play.')

        # wait finish
        while s.is_active():
            time.sleep(0.01) # 1ms
        
        # closing stream
        s.stop_stream()
        s.close()
        wf.close()
        p.terminate()
        print('finished sound play.')


    def play(self, wavfile):
        # threading
        audio_thread = threading.Thread(target=player.playsound, args=(wavfile,))
        audio_thread.start()


if __name__ == '__main__':
    file = sys.argv[1]

    player = SoundPlayer()
    player.play(file)
    # player.playsound(file)

