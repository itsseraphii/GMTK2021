from pygame.mixer import music as Music
from enum import IntEnum
from utils.constants import DATA_PATH

MAIN_MUSIC_PATH = DATA_PATH + "/music/main.mp3"
LEVEL_MUSIC_PATH = DATA_PATH + "/music/level.mp3"
JINGLE_PATH = DATA_PATH + "/music/jingle.mp3"
TIME_OVER_MUSIC_PATH = DATA_PATH + "/music/timeOver.mp3"
CREDITS_MUSIC_PATH = DATA_PATH + "/music/credits.mp3"

class MusicEvents(IntEnum):
    LEVEL_OVER = 1
    JINGLE_OVER = 2
    CREDITS_OVER = 3

def StartMusicMenu():
    Music.load(MAIN_MUSIC_PATH)
    Music.set_volume(0.5)
    Music.play(-1) # Loop forever

def StartMusicLevel():
    Music.load(LEVEL_MUSIC_PATH)
    Music.set_endevent(MusicEvents.LEVEL_OVER)
    Music.set_volume(0.5)
    Music.play() # Play once

def StartMusicJingle():
    Music.load(JINGLE_PATH)
    Music.set_endevent(MusicEvents.JINGLE_OVER)
    Music.set_volume(0.5)
    Music.play()

def StartMusicTimeOver():
    Music.load(TIME_OVER_MUSIC_PATH)
    Music.set_volume(0.5)
    Music.play(-1)

def StartMusicCredits():
    Music.load(CREDITS_MUSIC_PATH)
    Music.set_endevent(MusicEvents.CREDITS_OVER)
    Music.set_volume(0.5)
    Music.play()

def ProcessMusicEvents(event):
    Music.set_endevent() # Reset triggered event

    if (event == MusicEvents.LEVEL_OVER):
        StartMusicJingle()
    elif (event == MusicEvents.JINGLE_OVER):
        StartMusicTimeOver()
    elif (event == MusicEvents.CREDITS_OVER):
        StartMusicMenu()