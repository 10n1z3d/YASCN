#!/usr/bin/env python
#
# YASCN (Yet Another Song Change Notifier)
#
# Simple script which uses notify-osd to notify you about
# song change in different media players.
#
# Currently supports only Exaile, Banshee, Rhythmbox and Audacious.
#
# Copyright (C) 2009 10n1z3d <10n1z3d[at]w[dot]cn>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import time
import pynotify
from os import popen

INTERVAL = 5    # Interval between song change checks
last_song = ''

def get_player_info():
    '''Determines the player currently running and queries the song name
    then returns the player name and song name.
    '''
    current_player = None
    current_song = None
    players = {'exaile': 'exaile --get-title',
               'banshee': 'banshee --query-title',
               'rhythmbox': 'rhythmbox-client --print-playing',
               'audacious': 'audtool2 --current-song'}

    for player, cmd in players.iteritems():
        if player in popen('ps -A | grep %s' % player).readline():
            current_player = player
            current_song = popen(cmd).readline().replace('\n', '')
            break

    return (current_player, current_song)

def show_notification(current_player, current_song):
    '''Shows notification with the currently playing song.'''
    pynotify.init("yascn")
    notification = pynotify.Notification("Now playing", current_song,
                                         current_player)
    notification.show()

def main():
    '''Main loop'''
    global last_song
    
    while True:
        try:
            (current_player, current_song) = get_player_info()
            if current_player != None and current_song != None:
                if current_song != last_song:
                    show_notification(current_player, current_song)
                    last_song = current_song
            time.sleep(INTERVAL)
        except (KeyboardInterrupt, SystemExit):
            exit(0)

if __name__ == '__main__':
    main()
