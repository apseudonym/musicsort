import os
from mutagen.id3 import ID3

musicroot = os.path.join(os.path.expanduser('~'), 'Music')

albums = []
illegal = r'\/*?:"<>|'

def cleanSort():
	print('Beginning sorting process, this might take a few minutes...')
	
	os.chdir(musicroot)

	getFolders(musicroot)

	for i in albums:
		path = os.path.join(musicroot, i)
		print(i)
		songs = findSongs(path)
		song = songs[0]
		songInfo = ID3(song)
		try:
			songArtist = songInfo['TPE1'].text[0]
			songAlbum = songInfo['TALB'].text[0]
			sort(songArtist, songAlbum, i)
		except KeyError:
			print('Problem with tags on: {0}, consider retagging and try again'.format(os.path.split(i)[1]))
			
	emptySweep(musicroot)
	print('Done sorting!')
		
def findSongs(location):
	songs = []
	for i in os.listdir(location):
		if '.mp3' in i:
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
		#os.mkdir(albumlocation)
		try:
			for i in os.listdir(directory):
				os.renames(os.path.join(directory, i), os.path.join(albumlocation, i))
		except: 
			print('\tSome file already exisits, you may want to look at your music')
		

def emptySweep(location):
	print('Cleaning up...')
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
        

def getFolders(location):
	directories = []
	containsMusic = False
	for i in os.listdir(location):
		if '.mp3' in i:
			return location
		if os.path.isdir(os.path.join(location, i)):
			directories.append(os.path.join(location, i))
	for directory in directories:
		check = getFolders(os.path.join(location, directory))
		if check:
			albums.append(check)
	

if __name__ == '__main__':
	cleanSort()
