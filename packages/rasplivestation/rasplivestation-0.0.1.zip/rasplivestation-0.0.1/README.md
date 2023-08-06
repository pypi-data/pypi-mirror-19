RaspLiveStation : a little usefull package to launch at distance a stream on your Raspberry Pi by Krounet
=========================================================================================================

This package use paramiko and livestreamer Python 2.7 packages.

Paramiko is a Python implementation of the SSHv2 protocol : http://www.paramiko.org/
Livestreamer is a command-line utility use to watch streams into a video player (player, omxplayer,etc...) with an API which can work with Python : http://docs.livestreamer.io/

To install Paramiko : pip install paramiko

***Warning***

It would be a little difficult to install paramiko, because this package have a dependance with the package cryptography, which use any C libraries bindings(OpenSSL). Check https://cryptography.io/en/latest/installation/
and https://cryptography.io/en/latest/hazmat/bindings/ to have more information about this. On windows, it could be interesting to install environment like python(x,y) which include paramiko.

To install Livestreamer on Debian/Ubuntu (on your Raspberry) : apt-get install livestreamer
To install Livestreamer Python package: pip install livestreamer

To install RaspLiveStation package : pip install rasplivestation

Enjoy :)

This package is under WTFPL licence.
