import omni.audioplayer  # need "omni.audioplayer" extension.
import time
import asyncio

# ----------------------------------------------.
# AudioPlayer.
# ----------------------------------------------.
class AudioPlayer:
    _player = None
    _filePath = None
    _loadSuccess = False
    _loadBusy = False

    def __init__(self):
        pass

    def startup (self):
        self._player = omni.audioplayer.create_audio_player()

    def shutdown (self):
        self.stop()
        self._player = None

    def _file_loaded (self, success : bool):
        self._loadSuccess = success
        if success:
            print("load success!")
            soundLength = self._player.get_sound_length()
            print("sound length : " + str(soundLength) + " sec")
        else:
            print("load failed...")
        self._loadBusy = False

    # Load sound from file.
    def loadFromFile (self, filePath : str):
        self._loadSuccess = False
        if self._player == None:
            return
        self._filePath = filePath
        self._loadBusy = True
        self._player.load_sound(filePath, self._file_loaded)

    # Wait for it to finish loading.
    def isLoad (self):
        while self._loadBusy:
            time.sleep(0.1)
        return self._loadSuccess

    # Called when playback is finished.
    def _play_finished (self):
        print("play finished.")

    # Play sound.
    def play (self):
        if self._player == None:
            return False

        self._player.play_sound(self._filePath, None, self._play_finished, 0.0)

    # Stop sound.
    def stop (self):
        if self._player != None:
            self._player.stop_sound()

# ----------------------------------------------.
# Initialize AudioPlayer.
audio = AudioPlayer()
audio.startup()

# Load sound file.
# Specify an Audio file name that matches your environment.
audio.loadFromFile("./audio/HitWall.ogg")

if audio.isLoad():
    for i in range(3):
        # Play sound.
        audio.play()

        # Wait one seconds.
        time.sleep(1.0)

# Terminate AudioPlayer.
audio.shutdown()


