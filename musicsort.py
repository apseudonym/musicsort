import os, sys
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC

musicroot = os.path.join(os.path.expanduser('~'), 'Music')

folders = []
illegal = r'\/*?:"<>|'

def cleanSort():
	print('Beginning sorting process, this might take a few minutes...')
	
	os.chdir(musicroot)

	getMusicFolders(musicroot)
				
	for i in folders:
		path = os.path.join(musicroot, i)
		print(i)
		songs = findSongs(path)
		song = songs[0]
		songInfo = getSongInfo(song)
		try:
			songArtist = songInfo['artist'][0]
			songAlbum = songInfo['album'][0]
		except KeyError:
<<<<<<< HEAD
			songInfo = tagMusic(i, songs)
			songArtist = songInfo['artist']
			songAlbum = songInfo['album']
		sort(songArtist, songAlbum, i)

	print('Cleaning up...')	
=======
			print('Problem with tags on: {0}, consider retagging and try again'.format(os.path.split(i)[1]))
	
	print('Cleaning up...')		
>>>>>>> 6053b57b538bea21dd70ec4cbec29805fc5c0a24
	emptySweep(musicroot)
	print('Done sorting!')

def tagMusic(location, songs):
        print('Problem with tags on "{0}", please manually enter information'.format(os.path.split(location)[1]))
        artist = input('Artist name? \n')
        album = input('Album name? \n')
        for song in songs:
                songInfo = getSongInfo(song)
                songInfo['artist'] = artist
                songInfo['album'] = album
                songInfo.save()
        return {'artist': artist, 'album': album}
		
def findSongs(location):
	songs = []
	for i in os.listdir(location):
		if isSong(i):
			songs.append(os.path.join(location, i))
	return songs


def sort(artist, album, directory):
	for i in illegal:
		artist = artist.replace(i, '')
		album = album.replace(i, '')
	artistlocation = os.path.join(musicroot, artist)
	albumlocation = os.path.join(musicroot, artist, album)
	try:
		os.mkdir(artistlocation)
	except:
		pass
	try:
		os.rename(directory, albumlocation)
	except:
		try:
			for i in os.listdir(directory):
				os.renames(os.path.join(directory, i), os.path.join(albumlocation, i))
		except: 
			print('\tSome file already exisits, you may want to look at your music')


def getMusicFolders(location):
	directories = []
	for i in os.listdir(location):
		if isSong(i):
			return location
		if os.path.isdir(os.path.join(location, i)):
			directories.append(os.path.join(location, i))
	for directory in directories:
		check = getMusicFolders(os.path.join(location, directory))
		if check:
			folders.append(check)


def getSongInfo(song):
	if '.mp3' in song:
			songInfo = EasyID3(song)
	if '.flac' in song:
			songInfo = FLAC(song)
	return songInfo


def isSong(file):
	if '.mp3' in file or '.flac' in file:
		return True
	return False


def emptySweep(location):
	items = os.listdir(location)
	if items == []:
		return True
	for i in items:
		nextleaf = os.path.join(location, i)
		if os.path.isdir(nextleaf):
			check = emptySweep(nextleaf)
			if check:
				os.removedirs(nextleaf)
	return False


if __name__ == '__main__':
	cleanSort()
