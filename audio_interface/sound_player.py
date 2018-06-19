# -*- coding: utf-8 -*-
import pyaudio
import wave
import threading
import sys
import codecs
import time

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
        wfinfo = wf.getparams()
        self.show_wavinfo(wfinfo)
        p = pyaudio.PyAudio()
        try:
            s = p.open(format=p.get_format_from_width(wfinfo[1]),
                       channels=wfinfo[0],
                       rate=wfinfo[2],
                       output=True)

            # play stream
            input_data = wf.readframes(CHUNK)
            logger.i('started blocking sound play.')
            while len(input_data) > 0:
                # controls
                # stop
                if self.event_stop.is_set():
                    logger.i('stop sound.')
                    break
                # pause
                if self.event_pause.is_set():
                    logger.i('pause sound.')
                    while self.event_pause.is_set():
                        time.sleep(0.1)
                        if self.event_stop.is_set():
                            # finish
                            break
                # write sound
                output_data = self.mod_main(input_data)
                s.write(output_data)
                input_data = wf.readframes(CHUNK)

        finally:
            # close stream
            s.stop_stream()
            s.close()
            wf.close()
            p.terminate()
            logger.i('finished sound play.')

    def mod_main(self, input_data):
        #     # logger.d('non-blocking play ({}, {}, {}, {})'.format(in_data,
        #     #                                                      frame_count, time_info, status))
        return input_data

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


        # def non-blocking callback
        # def callback(in_data, frame_count, time_info, status):
        #     input_data = wf.readframes(frame_count)

        #     # stop
        #     if self.event_stop.is_set():
        #         logger.i('stop sound.')
        #         return (input_data, pyaudio.paComplete)
        #     # pause
        #     if self.event_pause.is_set():
        #         logger.i('pause sound.')
        #         while self.event_pause.is_set():
        #             time.sleep(0.1)
        #             if self.event_stop.is_set():
        #                 # finish
        #                 break

        #     # play
        #     # logger.d('non-blocking play ({}, {}, {}, {})'.format(in_data,
        #     #                                                      frame_count, time_info, status))

        #     # mod wav
        #     output_data = ''
        #     for input_string in input_data:
        #         if input_string == '':
        #             continue

        #         print('is = {}'.format(input_string))
        #         if wfinfo[0] == 2:
        #             input_value = struct.unpack('h', input_string)
        #         else:
        #             input_value = input_string

        #         # effects
        #         output_value = input_value

        #         # write
        #         if wfinfo[0] == 2:
        #             output_string = struct.pack(
        #                 'h', output_value, output_value)
        #         else:
        #             output_string = struct.pack('h', output_value)
        #         output_data += output_string

        #     return (output_data, pyaudio.paContinue)


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
            dicmd['stop']()
            dicmd['exit']()
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
