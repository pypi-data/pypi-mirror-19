from untwisted.network import xmap
from subprocess import Popen
from vyapp.plugins.vyirc import IrcMode

class WhoCall(object):

    def __init__(self, irc, background='green', foreground='black', font='fixed', ):
        self.irc        = irc
        self.background = background
        self.foreground = foreground
        self.font       = font
        xmap(self.irc.con, 'CMSG', self.is_called)
        self.template  = "echo '%s' | dzen2 -p -bg %s -fg %s -l %s -fn %s" 

    def is_called(self, con, nick, user, host, target, msg):
        if self.irc.nick.lower() in msg.lower():
            Popen(self.template % ('%s messaged you.' % nick, self.foreground, 
                self.background, 2,  self.font) , shell=True)
