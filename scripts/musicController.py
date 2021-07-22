from pygame.mixer import music as Music
from enum import IntEnum
from utils.constants import DATA_PATH

BASE_VOLUME = 1
MAIN_MUSIC_PATH = DATA_PATH + "/music/main.mp3"
LEVEL_MUSIC_PATH = DATA_PATH + "/music/level.mp3"
JINGLE_PATH = DATA_PATH + "/music/jingle.mp3"
TIME_OVER_MUSIC_PATH = DATA_PATH + "/music/timeOver.mp3"
BOSS_MUSIC_PATH = DATA_PATH + "/music/boss.mp3"
CREDITS_MUSIC_PATH = DATA_PATH + "/music/credits.mp3"

class MusicEvents(IntEnum):
    START_JINGLE = 1
    START_TIME_OVER = 2
    START_MENU = 3

def StartMusicMenu():
    Music.load(MAIN_MUSIC_PATH)
    Music.set_volume(BASE_VOLUME * 0.5)
    Music.play(-1) # Loop forever

def StartMusicLevel():
    Music.load(LEVEL_MUSIC_PATH)
    Music.set_endevent(MusicEvents.START_JINGLE)
    Music.set_volume(BASE_VOLUME * 0.5)
    Music.play() # Play once

def StartMusicJingle():
    Music.load(JINGLE_PATH)
    Music.set_endevent(MusicEvents.START_TIME_OVER)
    Music.set_volume(BASE_VOLUME * 0.5)
    Music.play()

def StartMusicTimeOver():
    Music.load(TIME_OVER_MUSIC_PATH)
    Music.set_volume(BASE_VOLUME * 0.5)
    Music.play(-1)

def StartMusicBoss():
    Music.load(BOSS_MUSIC_PATH)
    Music.set_endevent(MusicEvents.START_MENU)
    Music.set_volume(BASE_VOLUME * 0.7)
    Music.play()

def StartMusicCredits():
    Music.load(CREDITS_MUSIC_PATH)
    Music.set_endevent(MusicEvents.START_MENU)
    Music.set_volume(BASE_VOLUME * 0.6)
    Music.play()

def ProcessMusicEvents(event):
    Music.set_endevent() # Clear triggered event

    if (event == MusicEvents.START_JINGLE):
        StartMusicJingle()
    elif (event == MusicEvents.START_TIME_OVER):
        StartMusicTimeOver()
    elif (event == MusicEvents.START_MENU):
        StartMusicMenu()