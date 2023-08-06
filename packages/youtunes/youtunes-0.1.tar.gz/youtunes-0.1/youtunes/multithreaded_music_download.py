# encoding=utf8 
import urllib2
import urllib
import sys
import re
import youtube_dl
import subprocess
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup 
import os
import eyed3
from threading import Thread, Lock
import requests
import errno

# global mutex for the metadata
metadata_lock = Lock()
USER = os.path.expanduser("~")
DEFAULT_SAVE_NAME = '{}/Downloads/default_music_download_name'.format(USER)
FRONT_COVER = 3


def set_defaults():
	reload(sys)  
	sys.setdefaultencoding('utf8')


def cap_string_length(input_string, max_len):
	if (len(input_string) > max_len - 3): return input_string[:max_len - 3] + "..."
	return input_string


def get_result_links(song_choice, all_links):
	query_string = urllib.urlencode({"search_query" : song_choice})
	html_content = urllib2.urlopen("http://www.youtube.com/results?" + query_string).read()

	all_data = re.findall(r'href=\"(\/watch\?v=.{11})\"[^>]+title=\"([^\"]*)\".+Duration: (\d+:\d+).+<a href="/(?:user|channel)/[^>]*>([^<]*)<.+<li>(\S+) views</li>', html_content)

	h = HTMLParser()
	for entry in all_data:
		all_links.append([h.unescape(data) for data in entry])


def print_video_options(all_links):

	num_links = len(all_links)

	for i in range(num_links):
		entry = all_links[i]

		# number) title duration channel views
		print '{:2d}) {:50s} {:8s} {:30s} {:>15s} views'.format(i + 1, cap_string_length(entry[1], 50), entry[2], cap_string_length(entry[3], 30), entry[4])

	print '{:2d}) Not what you\'re looking for? Search using different keywords.'.format(num_links + 1)


def get_link(all_links):

	print_video_options(all_links)

	while (True):
		choice = raw_input("\nChoose a video: ")
		if (not choice.isdigit()): 
			print "Choice not a valid integer."
			continue
		
		choice = int(choice) - 1
		if (choice < 0 or choice > len(all_links)): 
			print "Choice not in range."
			continue

		return choice


def print_metadata_options(all_metadata):

	for i in range(len(all_metadata)):
		entry = all_metadata[i]

		# number) title artist album
		print '{:2d}) Title: {:50s} Artist: {:50s} Album: {:30s}'.format(i + 1, cap_string_length(entry[0], 50), cap_string_length(entry[1], 50), entry[2])


def prompt_for_metadata_change(metadata):

	while (True):

		quit_choice = raw_input("\nIs there anything about this metadata you'd like to change (Y / N)? ").lower()
		if (quit_choice == 'n'): return
		if (quit_choice == 'y'): break

		print 'Please enter a valid option (Y / N).'

	while (True):

		print '1) Title: {}'.format(metadata[0])
		print '2) Artist: {}'.format(metadata[1])
		print '3) Album: {}'.format(metadata[2])
		print '4) Album Art URL: {}'.format(metadata[3])
		print '5) I\'m finished.'
		
		choice = raw_input('\nWhat do you want to change (enter the corresponding integer) ? ')

		if (not choice.isdigit()): 
			print "Choice not a valid integer."
			continue
		
		choice = int(choice) - 1
		if (choice == len(metadata)): return
		if (choice < 0 or choice > len(metadata)): 
			print "Choice not in range."
			continue

		metadata[choice] = raw_input('Enter new data: ')



def get_metadata(all_metadata):

	print_metadata_options(all_metadata)

	while (True):
		choice = raw_input("\nChoose metadata option (enter to put in manually): ")
		if (choice == ""): return []

		if (not choice.isdigit()): 
			print "Choice not a valid integer."
			continue
		
		choice = int(choice) - 1
		if (choice < 0 or choice >= len(all_metadata)): 
			print "Choice not in range."
			continue

		metadata = all_metadata[choice]
		prompt_for_metadata_change(metadata)
		return metadata


def get_link_metadata(i, link, all_metadata):

	title_artist = [s.strip() for s in link.get_text().replace(u'\xa0', u' ').split(" by ")]
	
	# change title_artist to accommodate iTunes sorting
	featured_artist_index = title_artist[1].find(' (Ft. ')
	if (featured_artist_index != -1): # there is a featured artist
		# then take if off of the artist and attach it to the title
		artists = re.findall(r' \(Ft\. ([^\)]*)\)', title_artist[1])[0]
		title_artist[1] = title_artist[1][:featured_artist_index]
		title_artist[0] += " (feat. " + artists + ")"

	req = urllib2.Request(link.get('href'), headers={'User-Agent' : "Magic Browser"}) 
	html_content = urllib2.urlopen(req).read()

	album_info = re.findall(r"\"Primary Album\":\"([^\"]*)\"", html_content)
	album = "" if album_info == [] else album_info[0]

	# try two different options
	album_art_info = re.findall(r'class=\"song_album-album_art\" title=\"{}\">[^<]*<img \S+ src=\"([^\"]*)\"'.format(album), html_content)
	if (album_art_info == []): album_art_info = re.findall(r"content=\"([^\"]*)\" property=\"twitter:image\"", html_content)
	album_art_url = "" if album_art_info == [] else album_art_info[0]

	metadata_lock.acquire()
	all_metadata[i] = (title_artist + [album, album_art_url])
	metadata_lock.release()


def search_for_song_metadata(song_choice, all_metadata, threads):

	url = "https://genius.com/search?" + urllib.urlencode({"q" : song_choice})
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
	html_content = urllib2.urlopen(req).read()

	soup = BeautifulSoup(html_content, 'html.parser')
	soup.prettify()

	links = soup.find_all("a", class_=" song_link")
	if (links == []): return

	# used to maintain the order of the links
	num_links = len(links)
	all_metadata += ([None] * num_links)
	for i in range(len(links)): threads.append(Thread(target=get_link_metadata, args=(i, links[i], all_metadata)))


def get_manual_metadata():
	title = raw_input("Specify song title: ")
	artist = raw_input("Specify song artist (enter for \"Unknown Artist\"): ")
	album = raw_input("Specify song album (enter for \"Unknown Album\"): ")
	album_art_url = raw_input("Specify url for album art (enter for no album art): ")

	return [title, artist, album, album_art_url]


def update_song_info(album, artist, album_art_url):
	# change the album and artist info
	f = eyed3.load("{}.mp3".format(DEFAULT_SAVE_NAME))
	f.tag.album = unicode(album)
	f.tag.artist = unicode(artist)
	if (album_art_url != ""):
		try:
			with open('{}/Downloads/{}_{}_album_art.jpg'.format(USER, title, artist), 'rb') as image:
				f.tag.images.set(FRONT_COVER, image.read(), 'image/jpeg')
		except:
			print "Invalid album art url. Couldn't download jpg."
	f.tag.save()


def download_album_art(album_art_url, title, artist):
	# download the album art
	if (album_art_url == ""): return

	try:
		newfile = os.open('{}/Downloads/{}_{}_album_art.jpg'.format(USER, title, artist), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
		with os.fdopen(newfile, 'wb') as image:
	        # Using `os.fdopen` converts the handle to an object that acts like a
	        # regular Python file object, and the `with` context manager means the
	        # file will be automatically closed when we're done with it.
			r = requests.get(album_art_url)
			image.write(r.content)
	except OSError as e:
		if e.errno == errno.EEXIST:  # Failed as the file already exists.
			pass
		else:  # Something unexpected went wrong so reraise the exception.
			print 'Failed to download the album art at {}.'.format(album_art_url)


def download(ydl_opts, link):
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([link])

			

if __name__ == "__main__":

	set_defaults()

	ydl_opts = {
	    'quiet': 'True',
	    'no_warnings': 'True',
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	}

	# continuously prompts for song choices
	while (True):

		threads = []

		# prompts for the song
		song_choice = raw_input("\nWhat song do you want to search for (enter to quit)? ")
		if (song_choice == ""):
			print "Done downloading songs. Exiting program."
			break

		all_links = []
		all_metadata = []
		threads.append(Thread(target=get_result_links, args=(song_choice, all_links)))
		search_for_song_metadata(song_choice, all_metadata, threads)

		for thread in threads: thread.start()
		for thread in threads: thread.join()

		if (all_links == []):
			print "Couldn't find the requested song.\n"
			continue

		link_choice = get_link(all_links)
		if (link_choice == len(all_links)):
			continue
		link = "http://www.youtube.com" + all_links[link_choice][0]
		
		# immediately begin downloading while user selects metadata
		ydl_opts['outtmpl'] = '{}.%(ext)s'.format(DEFAULT_SAVE_NAME)
		t1 = Thread(target=download, args=(ydl_opts, link))
		t1.start()

		metadata = []
		if (all_metadata == []):
			print "No metadata found for this song on Genius."
		else:
			metadata = get_metadata(all_metadata)

		if (metadata == []): metadata = get_manual_metadata()
		title, artist, album, album_art_url = metadata

		print '\nDownloading \"{}\"...'.format(title)
		t2 = Thread(target=download_album_art, args=(album_art_url, title, artist))
		t2.start()

		# wait for album art and song to finish downloading
		t1.join()
		t2.join()

		update_song_info(album, artist, album_art_url)

		automatically_add_location = "{}/Music/iTunes/iTunes Media/Automatically Add to iTunes.localized/{}.mp3".format(USER, title)

		# move from Downloads to Automatically Add to iTunes
		os.rename("{}.mp3".format(DEFAULT_SAVE_NAME), automatically_add_location)

		print "\nFinished adding \"{}\" to the iTunes library.".format(title)





