# ogger.py
#
# Plays .ogg audio files from directory
#
# Written & tested on Occidentalis v0.2 from Adafruit.com
#
#
# Based on script from:
# http://www.raspberrypi.org/phpBB3/viewtopic.php?f=32&t=10240
# Note: runs on Linux (needs curses).
# Note: will not run correctly from Idle.

import os
import sys
import pygame
import curses

# MUSIC_PATH = './x-1' # folder where .ogg files are



def print_help():
    ''' Print keymappings. '''
    stdscr.addstr('b - pause\n')
    stdscr.addstr('n - next\n')
    stdscr.addstr('v - back\n')
    stdscr.addstr('q - quit\n')
    stdscr.addstr('h - help\n')


def write_positions(music, positions={}, blank=False):
    ''' Write positions to file. Create empty dict if blank. '''
    if blank:
        folders = music.keys()
        folders.sort()
        positions = {'folder': folders[0]}
        for folder in folders:
            positions[folder] = {'track':0, 'position':0}
        print 'writing blank positions'
    f = open('positions.txt', 'w')
    f.write(str(positions))
    f.close()
    print positions
    return positions

    
def get_music():
    ''' Return dictionary of directories and .ogg files.
        music = {'dir':[file1, file2], ...}'''

    music = {}
    listdir = os.listdir(os.getcwd())
    for name in listdir:
        path = os.path.join(os.getcwd(), name)
        if os.path.isdir(path):
            raw_filenames = os.listdir(path)
            music_files = []
            for filename in raw_filenames:
               if filename.endswith('.ogg'):
                  music_files.append(filename)
            if len(music_files) >0:
                music_files.sort()
                music[name] = music_files
    try: # see if folders unchanged
        f = open('music.txt', 'r')
        l = f.readlines()
        l = l[0].strip()
        f.close()
    except:
        print 'unable to open or find music.txt'
        l = None

    #print type(l), len(l)
    #print
    #print type(str(music)), len(str(music))    
    if l == str(music):
        print 'music checks, loading positions'
        try: # load positions
            f = open('positions.txt', 'r')
            positions = f.readlines()
            f.close()
        except:
            print 'unable to open or find positions.txt'
            positions = write_positions(music, blank=True)
    else:
        print 'new music found, writing music.txt'
        f = open('music.txt', 'w')
        f.write(repr(music))
        f.close()
        positions = write_positions(music, blank=True)
    return music, positions



music, positions = get_music()
folders = music.keys()
folders.sort()

folder = folders.index(positions['folder'])
print music
print folders
print folder


#fileName, position = check_position()
   
# pygame.init()
# os.system('clear')

# init the curses screen and print info
stdscr = curses.initscr()
curses.noecho() # don't print keys to screen
curses.cbreak()   # use cbreak, does not require [Enter]
curses.curs_set(0) # turn off curser
print_help()

folder = 0
try:
   track = 0 #music_filenames.index(fileName)
except:
   track = 0
position = 0
paused = False

# set up the mixer
freq = 44100     # audio CD quality
bitsize = -16    # unsigned 16 bit
channels = 1     # 1 is mono, 2 is stereo
buffer = 1024    # number of samples (experiment to get right sound)
pygame.mixer.init(freq, bitsize, channels, buffer)
pygame.mixer.music.set_volume(0.5) # optional volume 0 to 1.0


while True:

    target = os.path.join(os.getcwd(), folder, music[folders[folder]][track])
    pygame.mixer.music.load(target) 
    pygame.mixer.music.play(0, position)
    stdscr.addstr('playing "%s" at %s sec.\n' % (music[folders[folder]][track], position))

    # loop while current track not finished
    while pygame.mixer.music.get_busy():
        pygame.time.wait(1) #slow loop down

        # python curses to 'get' keyboard input
        event = stdscr.getch()
        if event == ord("b"): # pause
            if not paused:
                paused = True
                pygame.mixer.music.pause()
                position = pygame.mixer.music.get_pos() / 1000
                #write_position(music_filenames[track], position)
                stdscr.addstr('paused at %s sec.\n' % position)
            else:
                paused = False
                pygame.mixer.music.unpause()
                stdscr.addstr('playing "%s"\n' % music[folders[folder]][track])
        if event == ord("n"): # next
            position = 0
            pygame.mixer.music.stop()
    
        if event == ord("v"): # back
            track = track - 2
            position = 0
            pygame.mixer.music.stop()
        if event == ord("q"): # quit
            pygame.mixer.music.stop()
            position = pygame.mixer.music.get_pos() / 1000
            #write_position(music_filenames[track], position)
            curses.nocbreak()
            curses.echo()
            curses.endwin()
            pygame.mixer.quit()
            os.system('reset')
            sys.exit()
        if event == ord("h"):
            print_help()

        stdscr.refresh()

   # increment track number         
    track = track + 1
    if track < 0:
        track = len(music[folder]) - 1
    if track == len(music[folder]):
        track = 0
    #write_position(music_filenames[track], 0)

