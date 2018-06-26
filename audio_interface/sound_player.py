# -*- coding: utf-8 -*-
import pyaudio
import wave
import threading
import sys
import codecs
import time
import numpy as np
import struct

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

        # effect params
        # mod_samplingrate is playing samplingrate.
        self.mod_samplingrate = 1.0
        self.mod_gain = 1.0

    def event_init(self):
        self.event_pause.clear()
        self.event_stop.clear()

    def show_wavinfo(self, wfinfo):
        logger.i(wfinfo)
        logger.i('wave file info')
        logger.i('channels = {}'.format(wfinfo[0]))
        logger.i('sampling width = {} byte'.format(wfinfo[1]))
        logger.i('frame rate = {} Hz'.format(wfinfo[2]))
        logger.i('frame count = {}'.format(wfinfo[3]))
        logger.i('sound time = {} s'.format((int)(wfinfo[3] / wfinfo[2])))

    def playsound(self, wavfile):
        if (wavfile == ""):
            logger.i('empty sound file.')
            return

        # open file
        logger.i('open file = {}'.format(wavfile))
        wf = wave.open(wavfile, 'rb')
        self.wfinfo = wf.getparams()
        self.show_wavinfo(self.wfinfo)
        try:
            p = pyaudio.PyAudio()
            s = p.open(format=p.get_format_from_width(self.wfinfo[1]),
                       channels=self.wfinfo[0],
                       rate=self.wfinfo[2],
                       output=True)

            # play stream
            input_data = wf.readframes(CHUNK)
            logger.i('started blocking sound play.')
            while len(input_data) > 0:
                if self.ctrl_sound():
                    break
                s.write(self.mod_sound(input_data))
                input_data = wf.readframes(CHUNK)

        finally:
            # close stream
            s.stop_stream()
            s.close()
            wf.close()
            p.terminate()
            logger.i('finished sound play.')

    def ctrl_sound(self):
        is_brake = False

        # stop action
        if self.event_stop.is_set():
            logger.i('stop sound.')
            is_brake = True
        # pause action
        if self.event_pause.is_set():
            logger.i('pause sound.')
            while self.event_pause.is_set():
                time.sleep(0.1)
                if self.event_stop.is_set():
                    # finish
                    break
            is_brake = False

        return is_brake

    def mod_sound(self, input_data):
        # logger.d('non-blocking play ({}, {}, {}, {})'.format(input_data)
        data = np.frombuffer(input_data, 'int16')

        # gain
        output_data = struct.pack("h" * len(data), *data)
        return output_data

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

    def set_samplingrate(self, rate):
        if rate > 0:
            self.mod_samplingrate = rate
        logger.i('set sampling rate = {}'.format(rate))


def myhelp():
    print(u'これはサウンドプレイヤーです。')
    print(u'')
    print(u'Usage: ')
    print(u'  play (ファイル) : 指定のファイルを再生する')
    print(u'  pause           : 一時停止')
    print(u'  resume          : 再生を再開する')
    print(u'  stop            : 再生を停止する')
    print(u'  ')
    print(u'  samplingrate    : サンプリング周波数を変更する')
    print(u'  __未定義__')
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
             'samplingrate': (lambda r: player.set_samplingrate(float(r))),
             'help': myhelp,
             'exit': sys.exit}
    # sys.stdout = codecs.getw_piter('utf_8')(sys.stdout)
    sys.stdout = codecs.getwriter('shift_jis')(sys.stdout)

    myhelp()
    while True:
        try:
            userinput = raw_input('audio interface >> ').lower()
        except KeyboardInterrupt:
            # ctrl + c
            dicmd['stop']()
            dicmd['exit']()
        logger.d('thread count = {}'.format(threading.active_count()))
        # enter only
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
