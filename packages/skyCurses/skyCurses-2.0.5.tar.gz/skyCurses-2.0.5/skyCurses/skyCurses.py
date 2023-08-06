#!/usr/bin/env python3

from redskyAPI.skychat import SkyChatClient
from winCurses import *

import re
from sys import argv, exit
from html import unescape
import curses
import os, signal
import simpleaudio
from .mplayer_wrapper import Player
import pafy
from time import sleep
from threading import Thread
import json

# CONSTANTS
HISTORY_SIZE = 256
CONFIG_DIR   = '.skycurses'

color_equiv = {
        '#ef4848' : ('cr', curses.COLOR_RED),
        '#bf00ff' : ('cm', curses.COLOR_MAGENTA),
        '#046380' : ('cb', curses.COLOR_BLUE),
        '#457dbb' : ('cc', curses.COLOR_CYAN),
        '#85c630' : ('cg', curses.COLOR_GREEN),
        '#ffab46' : ('cy', curses.COLOR_YELLOW),
        '#f5a6bf' : ('cr', curses.COLOR_RED),
        '#999999' : ('cw', curses.COLOR_WHITE),
        'grey'    : ('cw', curses.COLOR_WHITE),
        '#666666' : ('cw', curses.COLOR_WHITE),
        }

class SkyCurses(SkyChatClient):
    def on_creation(self):
        """ Used like the __init__ function here, but called after 
        SkyChatClient.__init__(self)
        """
        # load mplayer
        self.player      = Player()
        self.current_vid = ""

        # Curses init
        self.main_win         = Win()
        #                                               |-------POSITION--------|-------DIMENSION---------|
        self.title_win        = WTitle(self.main_win,    Coord(0,0),             Coord(3, (1, True)),      borders=[0]*8)
        self.notif_win        = WNotif(self.main_win,    Coord(3, 0),            Coord(1, (1, True)),      borders=[0]*8)
        self.player_win       = WTitle(self.main_win,    Coord(4, 0),            Coord(3, 3),              borders=[0]*8, title="◼")
        self.player_bar       = WProgress(self.main_win, Coord(4, 3),            Coord(3, -3),             borders=[0]*8, function=self._get_player_pos)
        self.chat_win         = WDisp(self.main_win,     Coord(7, 0),            Coord(-11, (0.85, True)), borders=[0]*8)
        self.input_win        = WInput(self.main_win,    Coord(-3, 0),           Coord(1, (1, True)),      borders=[0]*8)
        self.clients_list_win = WList(self.main_win,     Coord(7, (0.85, True)), Coord(-11, (0.15, True)), borders=[0]*8)
        self.typelist_win     = WNotif(self.main_win,    Coord(-4, 0),           Coord(1, (1, True)),      borders=[0]*8)
        self.main_win.refresh()
        self.input_win.start()
        self.player_bar.start()
        self.input_win.set_focus()

        # Multiple chats histories
        self.raw_msg_hist = {
                'main' : [],
                }
        self.chat_list = ['main']
        self.cur_chat  = 0
        self.chat_win.raw_hist = self.raw_msg_hist['main']
        self.unread = {}

        # Sounds
        self.sounds = {
                'nomi' : simpleaudio.WaveObject.from_wave_file(self._full_path("sounds/nomi.wav")),
                'msg'  : simpleaudio.WaveObject.from_wave_file(self._full_path("sounds/msg.wav")),
                'mp'   : simpleaudio.WaveObject.from_wave_file(self._full_path("sounds/mp.wav")),
                'end'  : simpleaudio.WaveObject.from_wave_file(self._full_path("sounds/end.wav")),
                }

        # Sent messages history
        self.history     = []
        self.history_pos = 0

        # config
        self.sound_on   = True
        self.player_on  = True
        self.chat_sound = { 'main' :  True }

        self._load()

    def on_connect(self):
        # Add youtube sync management
        self.ws.on('yt_sync', self.on_yt_sync)

        self._set_title()
        self.input_win.on_return   = self._process_message
        self.input_win.on_typing   = lambda x : self.set_typing(x) if not self.input_win.input_buff.startswith("/") and self.cur_chat == 0 else None
        self.input_win.on_spec_key = self._handle_spec_key

    def on_old_message(self, msg):
        self._disp_msg(msg)

    def on_message(self, msg):
        self._disp_msg(msg)

    def on_private_message(self, msg):
        if msg['pseudo'].lower() == self.pseudo.lower():
            chat = msg['cor'].lower()
        else:
            chat = msg['pseudo'].lower()
        self._disp_msg(msg, chat)

    def on_connected_list(self, msg):
        def prettify_time(seconds):
            if seconds < 10:
                return("actif")
            elif seconds < 60:
                return("%ds" % (seconds))
            elif seconds < 900:
                return("%dm" % (seconds // 60))
            else:
                return("AFK")

        msg['list'].sort(key=lambda x : x['right'], reverse=True)
        new_cli_list = [ ("%s (%s)" % (cli['pseudo'], prettify_time(cli['last_activity'])), color_equiv[cli['color']][1]) for cli in msg['list'] ]
        self.clients_list_win.load(new_cli_list)

    def on_yt_sync(self, msg):
        def _load_video():
            video = pafy.new("https://www.youtube.com/watch?v=%s" % (msg['id']))
            bestaudio = video.getbestaudio()
            if not bestaudio:
                return
            self.player.loadfile(bestaudio.url)
            for i in range(10):
                if self.player.time_pos != None:
                    break
                sleep(0.5)
            self.player.pause()
            self.player.seek(int(msg['cursor']))
            self.player_win.set_title("▶")

        if self.player_on: 
            if 'id' in msg and msg['id'] != self.current_vid:
                self.current_vid = msg['id']
                Thread(target=_load_video).start()
            elif len(msg) == 0:
                self.player.stop()
                self.player_win.set_title("◼")
    
    def on_typing_list(self, msg):
        if msg:
            self.typelist_win.disp("%s %s typing..." % (', '.join(msg), ('is' if len(msg) == 1 else 'are')))
        else:
            self.typelist_win.reset()

    def _disp_msg(self, msg, chat='main'):
        # Remove leading spaces
        message = unescape(msg['message'].lstrip(' '))
        # Smileys
        message = re.sub('<img[^>]*title="([^"]*)"[^>]*>', '\\1', message)
        # Images 
        message = re.sub('<img[^>]*src="([^"]*)"[^>]*>', 'http://redsky.fr\\1', message)
        # Quotes
        message = re.sub('<blockquote[^>]*><span.*>Par <b>([^<]*)</b>.*</span>(.*)</blockquote>(.*)$', '« \\1 : \\2 » → \\3', message)
        # Remaining HTML
        message = re.sub('<[^>]*>', '', message)
        # &lt; / &gt; / '\'
        message = message.replace('\\', '\\\\').replace('<', '\\<').replace('>', '\\>')

        pseudo_color = color_equiv[msg['color']][0]
        if chat not in self.chat_list:
            self.chat_list.append(chat)
            self.raw_msg_hist[chat] = []
            self.chat_sound[chat]   = True

        line = "<b><%s>%s</%s></b> [%d] %s" % (pseudo_color, msg['pseudo_html'], pseudo_color, msg['id'], message)
        if self.chat_list[self.cur_chat] == chat:
            self.chat_win.disp(line)
            self.input_win.set_focus()
        else:
            self.raw_msg_hist[chat].append(line)
            self.unread[chat] = 1 + (self.unread[chat] if chat in self.unread else 0)
            self._refresh_notif_win()

        # Audio notif
        if msg['pseudo'].lower() != self.pseudo.lower() and not msg.get('old'):
            if msg['message'].lower().find('@' + self.pseudo.lower()) != -1:
                self.sounds['nomi'].play()
            elif self.sound_on and self.chat_sound[chat]:
                if chat == 'main':
                    self.sounds['msg'].play()
                else:
                    self.sounds['mp'].play()


    def _process_message(self, msg):
        msg = msg.lstrip(' ')

        # Aliases
        for i in [ i for i in re.findall("%([^% ]+)%", msg) if i in self.alias ]:
            msg = re.sub('%' + i + '%', self.alias[i], msg)

        self.history.append(msg)
        if len(self.history) > HISTORY_SIZE:
            del self.history[0]
        self.history_pos = 0
        if msg.startswith('/') and self._execute(msg):
            return
        if self.cur_chat == 0:
            self.msgsend(msg)
        else:
            self.pmsend(self.chat_list[self.cur_chat], msg)

    def _execute(self, msg):
        commands = {
                'quit'       : self._quit,
                'quiet'      : lambda : self._set_sound(False),
                'unquiet'    : lambda : self._set_sound(True),
                'player'     : self._set_player,
                'mute'       : lambda : self._set_chat_sound(False),
                'unmute'     : lambda : self._set_chat_sound(True),
                'volume'     : self._set_player_volume,
                'alias'      : self._set_alias,
                'unalias'    : self._del_alias,
                }
        cmd, *args  = msg[1:].split(' ')
        if cmd in commands:
            try:
                commands[cmd](*args)
            except Exception:
                return(False)
            return(True)
        return(False)

    def _handle_spec_key(self, key):
        keys = {
                curses.KEY_PPAGE : lambda : self.chat_win.change_offset(-4),
                curses.KEY_NPAGE : lambda : self.chat_win.change_offset(4),
                curses.KEY_HOME  : lambda : self.chat_win.change_offset(0, True),
                curses.KEY_END   : lambda : self.chat_win.change_offset(-1, True),
                'CTRL_N'         : lambda : change_chat(1),
                'CTRL_P'         : lambda : change_chat(-1),
                curses.KEY_UP    : lambda : self._get_history(-1),
                curses.KEY_DOWN  : lambda : self._get_history(1),
                }

        def move_cursor(move):
            if move:
                self.input_win.buff_pos
            else:
                self.input_win.buff_pos = self.cusor_pos = 0

        def change_chat(shift):
            self.cur_chat = (self.cur_chat + shift) % len(self.chat_list)
            self.chat_win.offset   = 0
            self.chat_win.raw_hist = self.raw_msg_hist[self.chat_list[self.cur_chat]]
            self.chat_win.reload_history()
            self.chat_win.refresh_text()
            if self.chat_list[self.cur_chat] in self.unread:
                del self.unread[self.chat_list[self.cur_chat]]
            self._set_title()
            self._refresh_notif_win()

        if key in keys:
            keys[key]()

    def _refresh_notif_win(self):
        if self.unread:
            self.notif_win.disp(', '.join([ '%s(%d)' % (k, v) for (k, v) in self.unread.items() ]))
        else:
            self.notif_win.reset()

    def _set_title(self):
        self.title_win.set_title("SkyCurses, the unofficial curses SkyChat Client (%s) " % (self.chat_list[self.cur_chat]) + ("(Mute)" if not (self.sound_on and self.chat_sound[self.chat_list[self.cur_chat]]) else ""))

    def _set_sound(self, val):
        self.sound_on = val
        self._set_title()

    def _set_player(self, val):
        if type(val) == str:
            val = True if val.lower() == 'on' else False
        if val != self.player_on:
            self.player_on = val
            if not val:
                self.player.stop()
                self.current_vid = ""
                self.player_win.set_title("×")
            else:
                self.player_win.set_title("◼")
                self.msgsend("/yt sync")

    def _set_player_volume(vol):
        self.player.volume = vol

    def _set_chat_sound(self, val):
        self.chat_sound[self.chat_list[self.cur_chat]] = val
        self._set_title()

    def _get_player_pos(self):
        pos    = self.player.time_pos
        length = self.player.length
        if pos != None and length != None:
            return(pos / length if pos < length else 1)
        return(0)

    def _set_alias(self, name, *value):
        self.alias[name] = ' '.join(value)

    def _del_alias(self, name):
        del self.alias[name]

    def _get_history(self, delta):
        self.history_pos += delta
        if self.history_pos > 0:
            self.history_pos = 0
        elif -self.history_pos > len(self.history):
            self.history_pos = - len(self.history)
        
        self.input_win.set_content(self.history[self.history_pos] if self.history_pos else "")
        self.input_win.refresh_input()

    def _full_path(self, path):
        return(os.path.join(os.path.dirname(os.path.realpath(__file__)), path))

    def _get_user_path(self, path):
        user_dir = os.path.join(os.path.expanduser('~'), CONFIG_DIR)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        return(os.path.join(user_dir, path))

    def _load(self):
        with open(self._full_path('alias.json'), 'r') as f:
            self.alias = json.load(f)
        try:
            with open(self._get_user_path('alias.json'), 'r') as f:
                for (k, v) in { k : v for (k, v) in json.load(f).items() if k not in self.alias }.items():
                    self.alias[k] = v
        except FileNotFoundError:
            pass

    def _save(self):
        with open(self._get_user_path('alias.json'), 'w') as f:
            json.dump(self.alias, f)

    def _quit(self):
        self.ws.disconnect()
        curses.endwin()
        self.player.quit()
        self._save()
        self.sounds['end'].play().wait_done()
        os.kill(os.getpid(), signal.SIGKILL)
        exit(0)

            
def main():
    if 2 < len(argv) < 5:
        sc = SkyCurses(argv[1], argv[2], (argv[3] if len(argv) > 3 else 0))
        sc.run()
    else:
        print("Usage : %s <username> <password> [room]" % (argv[0]))


if __name__ == "__main__":
    main()
