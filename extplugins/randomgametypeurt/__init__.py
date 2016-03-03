# -*- coding: utf-8 -*-
#
# RandomGametypeUrT For Urban Terror plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2015 PtitBigorneau - www.ptitbigorneau.fr
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.1'

import b3
import b3.plugin
import b3.events
from b3.functions import getCmd

import random
import time, threading, thread

class RandomgametypeurtPlugin(b3.plugin.Plugin):
    
    _adminPlugin = None
    _gametypes = "ffa lms tdm ts ctf bomb ftl cah ft gg"
    _swaproleson = "bomb"
    _rgonoff = True
    _test = None
    _listgametypes = {
        'ffa':[0,'FreeForAll'],
        'lms':[1,'LastManStanding'],
        'tdm':[3,'TeamDeathMatch'],
        'ts':[4,'Team Survivor'],
        'ftl':[5,'Follow the Leader'],
        'cah':[6,'Capture and Hold'],
        'ctf':[7,'Capture The Flag'],
        'bomb':[8,'Bombmode'],
        'jump':[9,'Jump'],
        'ft':[10,'Freeze Tag'],
        'gg':[11,'GunGame']
    }
	
    def onLoadConfig(self):

        self._gametypes = self.getSetting('settings', 'gametypes', b3.STRING, self._gametypes)
        self._swaproleson = self.getSetting('settings', 'swaproleson', b3.STRING, self._swaproleson).split(' ')
        self._rgonoff = self.getSetting('settings', 'pluginactived', b3.BOOLEAN, self._rgonoff)

    def onStartup(self):

        self._adminPlugin = self.console.getPlugin('admin')
        
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False
        
        self.registerEvent('EVT_GAME_MAP_CHANGE', self.onGameMapChange)

        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = getCmd(self, cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

    def onGameMapChange(self, event):
        
        if self._rgonoff:

            self.randomgametype()
    
    def cmd_randomgametype(self, data, client, cmd=None):
        
        """\
        activate / deactivate randomgametypeurt
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
        
            if self._rgonoff:

                client.message('RandomGametypeUrT ^2activated')

            else:

                client.message('RandomGametypeUrT ^1deactivated')

            client.message('!randomgametype <on / off>')
            return

        if input[0] == 'on':

            if not self._rgonoff:

                self._rgonoff = True
                message = '^2activated'

            else:

                client.message('RandomGametypeUrT is already ^2activated') 

                return False

        if input[0] == 'off':

            if self._rgonoff:

                self._rgonoff = False
                message = '^1deactivated'

            else:
                
                client.message('RandomGametypeUrT is already ^1disabled')                

                return False

        client.message('RandomGametypeUrT %s'%(message))

    def randomgametype(self):

        self.grandom()

        lgametype = self._listgametypes[self.nextgametype]
        ngametype = lgametype[0]
        self.mgametype = lgametype[1] 

        thread.start_new_thread(self.wait, (60,))

        self.console.write("g_gametype %s"%(ngametype))

        if self.nextgametype in self._swaproleson:
        
            self.console.write("g_swaproles 1")

        else:

            self.console.write("g_swaproles 0")
    
    def grandom(self):

        ngametype = 0

        self.listgametype = self._gametypes.split(' ')

        for gametype in self.listgametype:
            ngametype += 1

        nagametype = random.randint(0, ngametype-1)

        x = nagametype
        self.nextgametype = self.listgametype[x]

        return

    def wait(self, temps):

        time.sleep(temps)
          
        self.console.write('bigtext "^2Random Next Gametype: ^4%s^7"'%self.mgametype)
