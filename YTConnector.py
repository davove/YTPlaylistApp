#YTConnector

__doc__ = """
YTConnector is for dealing with connections to Youtube for data. It deals with building the service,
getting credentials (OAuth), and acquiring the proper data. It will access local, private files, since 
I have not yet started to make a generalized version for users. 

Libraries I needed to download:
*pip install google-api-python-client
*pip install google-auth-oauthlib

Other dependencies:
*Need to get proper client_secrets.json from OAuth Client ID's

Files Created:
*Will make and access token.pickle inside the directory of the program. This is used for OAuth.

Methods:

*get_credentials(): acquires OAuth credentials for building services
*verified_credentials(): calls get_credentials but with an added layer of checking with user to make sure account is correct
*get_playlists(doVerify): returns a dictionary of playlists for your account with format title:id. Verifies to see correct account if needed
*get_playlist_items(playlist_name = None, playlistId = None, doVerify = False): gets a list of playlist items (songs) having specified a playlist by name or id 

Future changes:
*Deal with credentials in a smarter way - rather than every method having a potential to verify and get credentials itself, change credentials to a parameter
"""

import os, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class YTConnector:


	@staticmethod
	def get_credentials():
		'''
		returns the credentials needed to build a service. 
		'''

		credentials = None
		if os.path.exists("token.pickle"):
			print("Loading Credentials from token.pickle...")
			with open("token.pickle","rb") as file:
				credentials = pickle.load(file)

		if not credentials or not credentials.valid:
			if credentials and credentials.valid and credentials.refresh_token:
				print("Getting a new Access Token...")
				credentials.refresh(Request())
			else:
				print('Getting new credentials through OAuth...')
				flow = InstalledAppFlow.from_client_secrets_file(
					'client_secrets.json'
					,scopes = ['https://www.googleapis.com/auth/youtube.readonly']) 

				flow.run_local_server(port=8080, prompt = 'consent')
				credentials = flow.credentials
				with open("token.pickle", "wb") as file:
					pickle.dump(credentials, file)

		return credentials

	@staticmethod
	def verified_credentials():
		answer = None
		while answer != "y":
			credentials = YTConnector.get_credentials()
			yt = build('youtube', 'v3', credentials = credentials)
			title = yt.channels().list(part = 'snippet', mine = True).execute()['items'][0]['snippet']['title']
			#print(title)
			answer = input(f"input 'y' or 'n': is {title} the correct account?\n")
			if answer == "y":
				return credentials
			try:
				os.remove("token.pickle") #resets credentials		
			except FileNotFoundError:
				pass

	@staticmethod
	def get_playlists(doVerify = False):
		'''
		returns a dictionary of playlists with their titles as keys and their ids as values.
		'''
		if (not doVerify):
			credentials = YTConnector.get_credentials()
		else:
			credentials = YTConnector.verified_credentials()
		yt = build('youtube', 'v3', credentials = credentials)
		print("Connected to Youtube")
		res = {}
		pages = []
		pages.append(yt.playlists().list(part = 'snippet', mine = True, maxResults = 5).execute())
		# count = 1
		while True:
			# print(count)
			try:
				nextpg = pages[-1]['nextPageToken']
			except KeyError:
				break
			pages.append(yt.playlists().list(part = 'snippet', mine = True, maxResults = 5, pageToken = nextpg).execute())
			# count+=1
		for page in pages:
			for item in page['items']:
				res.update({item['snippet']['title']: item['id']})
		return res

	@staticmethod
	def get_playlist_items(playlist_name = None, playlist_id = None,doVerify = False):
		'''
		Precondition: at least one of playlist_name, playlist_id is not None
		Returns a list of PlaylistItems inside a given playlist, specified by title or id
		Robust for duplicate pages being returned, page tokens being bad sometimes
		'''
		try:
			playlists = YTConnector.get_playlists()
			if playlist_id == None:
				playlist_id = playlists[playlist_name]
		except KeyError:
			raise KeyError('name or id provided are not valid. Check spelling and capitalization!')
		if(playlist_id not in playlists.values()):
			raise KeyError('name or id provided are not valid. Check spelling and capitalization!')

		if (not doVerify):
			credentials = YTConnector.get_credentials()
		else:
			credentials = YTConnector.verified_credentials()
		yt = build('youtube','v3',credentials = credentials)
		req = yt.playlistItems().list(part = 'snippet', playlistId = playlist_id, maxResults = 5).execute()
		pages = []
		pages.append(req['items'])
		count = 1
		while True:
			print("pg "+str(count)+" added")
			try:
				nextpg = req['nextPageToken']
			except KeyError:
				break
			attempt = 0
			while attempt<=20:
				try:
					req = yt.playlistItems().list(part = 'snippet', playlistId = playlist_id, maxResults = 5, pageToken = nextpg).execute()
					break
				except Exception:
					print('Failed... Trying again...')
					time.sleep(1.1**attempt)
					attempt+=1
			if attempt>=21:
				raise Exception('Too many failures!')
			if req['items'] not in pages:
				pages.append(req['items'])
			else:
				print('Duplicate detected. Discarding request...')
			count+=1

		res = []
		for page in pages:
			for item in page:
				res.append(item)
		return res



if __name__ == "__main__":

	print("Starting test")


	# Testing credentials
	# credentials = YTConnector.verified_credentials()
	# yt = build('youtube', 'v3', credentials = credentials)
	# foo = yt.playlists().list(part = "snippet", mine = True)
	# bar = foo.execute()['items']
	# for i in bar:
	# 	print(i['snippet']['title'])

	playlists = YTConnector.get_playlists(doVerify = True).items()
	for playlist, PlID in playlists:
		print(playlist + ' : ' + PlID)

	target = input("What playlist would you like to access? Capitalization matters.\n")

	songs = YTConnector.get_playlist_items(playlist_name = target, doVerify = True)
	for song in songs:
		print(song['snippet']['title'])

	print("Finished test")



