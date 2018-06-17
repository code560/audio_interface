# -*- coding: utf-8 -*-
import pyaudio
import wave
import threading
import time
import atexit
import sys
import codecs

import util.logger as logger
# import pdb

# defines
CHUNK = 1024


class SoundPlayer:

    def __init__(self):
        # flags
        self.loop = False

        # event flags
        self.event_pause = threading.Event()
        self.event_stop = threading.Event()
        self.event_init()

    def event_init(self):
        self.event_pause.clear()
        self.event_stop.clear()

    def playsound(self, wavfile):
        if (wavfile == ""):
            logger.i('empty sound file.')
            return

        # open file
        logger.i('open file = {}'.format(wavfile))
        wf = wave.open(wavfile, 'rb')

        wfinfo = wf.getparams()
        logger.i(wfinfo)
        logger.i('wave file info')
        logger.i('channels = {}'.format(wfinfo[0]))
        logger.i('sampling width = {} byte'.format(wfinfo[1]))
        logger.i('frame rate = {} Hz'.format(wfinfo[2]))
        logger.i('frame count = {}'.format(wfinfo[3]))
        logger.i('sound time = {} s'.format((int)(wfinfo[3] / wfinfo[2])))

        # def non-blocking callback
        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            if self.event_stop.is_set():
                logger.i('stop sound.')
                return (data, pyaudio.paComplete)
            if self.event_pause.is_set():
                logger.i('pause sound.')
                while self.event_pause.is_set():
                    time.sleep(0.1)
                    if self.event_stop.is_set():
                        # finish
                        break
            else:
                # logger.d('non-blocking play ({}, {}, {}, {})'.format(in_data,
                #                                                      frame_count, time_info, status))
                pass
            return (data, pyaudio.paContinue)

        # open stream
        p = pyaudio.PyAudio()
        s = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                   channels=wf.getnchannels(),
                   rate=wf.getframerate(),
                   frames_per_buffer=CHUNK,
                   output=True,
                   stream_callback=callback)

        # play stream
        s.start_stream()
        logger.i('started non-blocking sound play.')

        # wait finish
        while s.is_active():
            time.sleep(0.1)

        # closing stream
        s.stop_stream()
        s.close()
        wf.close()
        p.terminate()
        logger.i('finished sound play.')

    def do_play(self, wavfile):
        # clear event flags
        self.event_init()
        # threading
        self.thread = threading.Thread(
            target=self.playsound, args=(wavfile,))
        self.thread.start()

    def do_pause(self):
        self.event_pause.set()

    def do_resume(self):
        self.event_pause.clear()

    def do_stop(self):
        self.event_stop.set()


def myhelp():
    print(u'これはサウンドプレイヤーです。')
    print(u'')
    print(u'Usage: ')
    print(u'  play (ファイル) : 指定のファイルを再生する')
    print(u'  pause           : 一時停止')
    print(u'  resume          : 再生を再開する')
    print(u'  stop            : 再生を停止する')
    print(u'  __未定義__')
    print(u'  help            : ヘルプを表示')
    print(u'  exit            : 終了する')


if __name__ == '__main__':
    # file = sys.argv[1]
    player = SoundPlayer()
    dicmd = {'play': player.do_play,
             'pause': player.do_pause,
             'resume': player.do_resume,
             'stop': player.do_stop,
             'help': myhelp,
             'exit': sys.exit}
    # sys.stdout = codecs.getw_piter('utf_8')(sys.stdout)
    sys.stdout = codecs.getwriter('shift_jis')(sys.stdout)

    myhelp()
    while True:
        userinput = raw_input('audio interface >> ').lower()
        logger.d('thread count = {}'.format(threading.active_count()))

        if len(userinput) == 0:
            continue

        cmds = userinput.split(' ')
        if cmds[0] not in dicmd:
            continue
        cmd = dicmd[cmds[0]]
        if len(cmds) > 1:
            cmd(cmds[1])
        else:
            cmd()

    player.play(file)
    # player.playsound(file)
