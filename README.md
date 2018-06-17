audio_interface
---
Maker Faire Tokyo 2018 (FXAT)  

# 環境
Python 2.7  
PyAudio==0.2.11  

> 実装/テスト環境はWindows10です。  

# 使い方

    $ py audio_interface\sound_player.py
    これはサウンドプレイヤーです。
    
    Usage:
      play (ファイル) : 指定のファイルを再生する
      pause           : 一時停止
      resume          : 再生を再開する
      stop            : 再生を停止する
      __未定義__
      help            : ヘルプを表示
      exit            : 終了する
    audio interface >> play test/se_coin.wav
    audio interface >> play test/se_firework2.wav
    audio interface >> pause
    audio interface >> resume
    audio interface >> play test/se_firework1.wav
    audio interface >> pause
    audio interface >> resume
    audio interface >> stop
    audio interface >> exit


