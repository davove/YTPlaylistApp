#YT Connector

__doc__ = """
YTConnector is for dealing with connections to Youtube for data. It deals with building the service,
getting credentials (OAuth), and acquiring the proper data. It will access local, private files, since 
I have not yet started to make a generalized version for users. 

Libraries I needed to download:
*pip install google-api-python-client
*pip install google-auth-oauthlib

Other dependencies:
*Having a functional API_Key that allows for your current IP
*Need to get proper client_secrets.json from OAuth Client ID's

Files Created:
*Will make and access token.pickle inside the directory of the program. This is used for OAuth.

Methods:
*get_credentials(): acquires OAuth credentials for building services

"""

import os, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def get_credentials():
	'''
	returns the credentials needed to build a service
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


if __name__ == "__main__":

	print("Starting test")

	# api_key = "AIzaSyBkjflmQCEl5sZh9Zfu90glHeFFjUHZUug"
	# yt = build('youtube', 'v3', developerKey = api_key)
	# wee = yt.channels().list(part = "snippet", id = "UCdXaunstBnHTQVeSCUZ5HtQ").execute()
	# print(wee)
	
	credentials = get_credentials()
	yt = build('youtube', 'v3', credentials = credentials)
	foo = yt.playlists().list(part = "snippet", mine = True)
	bar = foo.execute()['items']
	for i in bar:
		print(i['snippet']['title'])
	print("Finished test")



