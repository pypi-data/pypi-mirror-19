# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 15:58:56 2016

@author: croizerm
e-mail : krounet@gmail.com
"""
import livestreamer



class livestreamerLaunching:
    
    """Initialisation of the parameters. url : url of the stream (youtube,daylimotion,twitch,hitbox,etc.
    player : player that you want to use (omxplayer for the Raspberry, vlc,etc.)"""
    
    def __init__(self,url='',player='omxplayer -o hdmi'):
        
        self.url=url
        self.player=player
    
    
    def QualityList(self):
        """This function is used to obtain the stream quality"""        
        return livestreamer.streams(self.url).keys()
    
    
    def createCommand(self,quality):
        """This function return the command to launch the stream : livestreamer 
        (a call to the livestreamer API) + url of the stream + stream quality
        + player"""           
        return 'livestreamer %s %s -np "%s"'%(self.url,quality,self.player)

if __name__ == '__main__':
    
    """Test of the class livestreamerLaunching. It create the command to send, that's all"""    
    
    print 'it is a test'
    a=livestreamerLaunching('https://www.youtube.com/watch?v=DMv1PzQuawQ')
    list_quality=a.QualityList()
    for n_quality in range(len(list_quality)):
        print str(n_quality)+' : '+list_quality[n_quality]
    choose_quality=list_quality[input('choose quality [type a number] : ')]
    command=a.createCommand(choose_quality)
    print command
