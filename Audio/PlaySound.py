import omni.audioplayer  # need "omni.audioplayer" extension.
import time
from carb.eventdispatcher import get_eventdispatcher

# ----------------------------------------------------------.
# AudioPlayer (updated for newer omni.audioplayer API)
# ----------------------------------------------------------.
class AudioPlayer:
    def __init__(self):
        self._player = None
        self._filePath = None
        self._loadSuccess = False
        self._loadBusy = False
        self._subs = []

    def startup(self):
        self._player = omni.audioplayer.create_audio_player()
        # subscribe to load/ended events for this player instance
        if self._player is not None:
            ed = get_eventdispatcher()
            key = self._player.get_event_key()
            # observe loaded and ended events; use the same handler
            try:
                self._subs.append(ed.observe_event(event_name=omni.audioplayer.GLOBAL_EVENT_LOADED, on_event=self._on_event, filter=key))
                self._subs.append(ed.observe_event(event_name=omni.audioplayer.GLOBAL_EVENT_ENDED, on_event=self._on_event, filter=key))
            except Exception:
                # some older/newer setups may behave differently; ignore subscribe errors
                pass

    def shutdown(self):
        self.stop()
        # try to unsubscribe observers if possible
        for s in getattr(self, "_subs", []) or []:
            try:
                if hasattr(s, "unsubscribe"):
                    s.unsubscribe()
            except Exception:
                pass
        self._subs = []
        self._player = None

    def _on_event(self, event):
        # event.event_name expected; event may behave like a mapping for fields
        try:
            name = event.event_name
        except Exception:
            name = None

        if name == omni.audioplayer.GLOBAL_EVENT_LOADED:
            success = True
            try:
                success = event["success"]
            except Exception:
                try:
                    # try attribute access
                    success = getattr(event, "success", True)
                except Exception:
                    success = True

            self._loadSuccess = success
            self._loadBusy = False
            if success:
                print("load success!")
                try:
                    soundLength = self._player.get_sound_length()
                    print(f"sound length : {soundLength} sec")
                except Exception:
                    pass
            else:
                print("load failed...")

        elif name == omni.audioplayer.GLOBAL_EVENT_ENDED:
            # playback finished
            try:
                self._play_finished()
            except Exception:
                pass

    # Load sound from file. New API: no callback param — use events instead.
    def loadFromFile(self, filePath: str):
        self._loadSuccess = False
        if self._player is None:
            return
        self._filePath = filePath
        self._loadBusy = True
        # old code passed a callback; new API only accepts path
        self._player.load_sound(filePath)

    # Wait for it to finish loading.
    def isLoad(self):
        while self._loadBusy:
            time.sleep(0.1)
        return self._loadSuccess

    # Called when playback is finished.
    def _play_finished(self):
        print("play finished.")

    # Play sound. New API: only (path, startTime).
    def play(self):
        if self._player is None:
            return False
        if not self._filePath:
            return False
        self._player.play_sound(self._filePath)

    # Stop sound.
    def stop(self):
        if self._player is not None:
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


