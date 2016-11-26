#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import urllib2
import urllib
from bs4 import BeautifulSoup
import getpass

# Get BingXML file which contains the URL of the Bing Photo of the day
# idx = Number days previous the present day. 0 means current day, 1 means yesterday, etc
# n = Number of images predious the day given by idx
# mkt denotes your location. e.g. en-US means United States. Put in your country code
BingXML_URL = "http://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&mkt=en-GB"
page        = urllib2.urlopen(BingXML_URL)
BingXML     = BeautifulSoup(page, "lxml")

# For extracting complete URL of the image
Images    = BingXML.find_all('image')
ImageURL  = "https://www.bing.com" + Images[0].url.text
ImageName = Images[0].startdate.text+".jpg"

# All the images will be saved in '/home/[user]/Pictures/BingWallpapers/'
# username = getpass.getuser()
# path = '/home/' + username + '/Pictures/BingWallpapers/'
import glib
ruta = glib.get_user_special_dir(glib.USER_DIRECTORY_PICTURES)
path = ruta + '/BingWallpapers/'

if not os.path.exists(path):
	os.makedirs(path)
os.chdir(path)
if not os.path.isfile(ImageName):
	urllib.urlretrieve(ImageURL, ImageName)
	#gsettings_path = os.system('which gsettings')
	#if not os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri file:" + path + ImageName ):
	if not os.system("xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s " + path + ImageName ):
		os.system('notify-send "'+'Bing Wallpaper updated successfully'+'" "'+ Images[0].copyright.text.encode('utf-8') +'"')
		os._exit(1)
else:
	os.system('notify-send "'+'Bing Wallpaper unchanged'+'" "'+ Images[0].copyright.text.encode('utf-8') + ' Wallpaper already exists in wallpaper directory!'  +'"')
	os._exit(1)

os.system('notify-send "'+'Failed to change Bing Wallpaper'+'" "'+ "Please check the installation files again" +'"')
