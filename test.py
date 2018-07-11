# -*- coding: utf-8 -*-

from audio_interface.sound_player import SoundPlayer
import time

if __name__ == '__main__':
    try:
        sp = SoundPlayer.instance()

        for x in range(100):
            sp.do_play('test/se_coin.wav', True)
            # sp.set_loop(True)
            sp.do_play('test/se_jump.wav', True)

        time.sleep(5)
        sp.do_stop()
    except KeyboardInterrupt:
        sp.do_stop()
    else:
        sp.do_stop()
