#YTArchive

import os, pickle

import YTData

__doc__="""

A class for archiving playlists received from Youtube. Before being archived, the class will reference previous saves if possible,
in order to possibly recover some songs.

Collaborations:
*YTData for handling playlists/songs
*YTConnector imported for testing, isn't necessary and will be deleted in the future

Methods:
*dir_wrapper(func): a wrapper method for navigating in and out of directories as defined by playlist names
*load_playlist(self, playlist): 
*save_playlst(self, playlist): Creates a pickle file and a user-readable text file and saves them. Does this only after compiling
		together data from previous saved list with current list data to create a final playlist. If no previous
		file exists, just saves it
"""



def dir_wrapper(func):
	def wrapper(*args, **kwargs):
		for arg in args:
			if type(arg) == YTData.YTPlaylist:
				dirName = arg.name
				break			
		if dirName == None:
			dirName = args[1] #for if no playlist passed in
		directory = os.path.join(os.getcwd(), dirName)

		try:
			os.mkdir(directory)
			print("Making a new directory... " + dirName)
		except FileExistsError:
			pass
		os.chdir(directory)
		res = func(*args, **kwargs)
		os.chdir(os.pardir)
		return res
	return wrapper

@dir_wrapper
@staticmethod
def load_playlist(playlist_name):
	'''
	TODO: Loads a pickle for a playlist and passes it.
	'''

@dir_wrapper
@staticmethod
def save_playlist(playlist):
	
	'''
	TODO: Creates a pickle file and a user-readable text file and saves them. Does this only after compiling
	together data from previous saved list with current list data to create a final playlist. If no previous
	file exists, just saves it
	'''

	#NEW CASE
	file_name = playlist.name
	file_name = os.path.join(os.getcwd(), file_name)
	with open(file_name+'.pickle', "wb") as file: 
		pickle.dump(playlist, file)
	print(f'Pickled to {file_name}')

	with open(file_name, 'w', encoding = 'utf-8') as file:
		file.write(playlist.name+', on '+str(playlist.date_quieried)+'\n')
		file.write('ID: '+ playlist.ID + f'\n Contains {playlist.length} songs:\n\n')
		for URL,song in playlist.song_dict.items():
			file.write(f'{song.pos} - {song.name}\n Youtube.com/watch?v={song.URL}\n')
		file.write(f'\n\nThe amount of corrupt songs: {len(playlist.corrupt_song_list)}')
	print("file written!")



if __name__ == '__main__':

	import YTConnector

	print('running archive test...\nAcquiring playlist from Youtube') 

	target = 'Classical Bangers'

	res = YTConnector.get_playlist_items(playlist_name=target)
	print('got playlist')
	playlist = YTData.YTPlaylist('N/A',target,res)
	save_playlist(playlist)


